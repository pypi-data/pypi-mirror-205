import pandas as pd
import numpy as np
from pandiet import Reducer

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.ensemble import RandomForestClassifier
import shap

import faiss
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go  

class Autosegment:

    def __init__(self, df, sink_database, client, session_id,
                 user_id, override_k, k_min, k_max, 
                 excl, semi_supervised, prioritize, model_type) -> None:

        # global configurations
        self.data_raw = df
        self.sink_database = sink_database 
        self.client = client
        self.session_id = session_id

        # clustering configurations
        self.user_id = user_id
        self.k_min = k_min
        self.k_max = k_max 
        if isinstance(override_k, (int, float)):
            self.k = override_k 
        self.excl = excl 
        self.semi_supervised = semi_supervised
        self.prioritize = prioritize 
        self.model_type = model_type

    @staticmethod
    def prioritize_df(df, prioritize):
        """Adjusts input data for prioritization (semi-supervised) methods.

        Args:
            df (DataFrame): DataFrame containing features, be sure column names are features.
            prioritize (dict): Dictionary containing features to prioritize and prioritization coefficients.

        Returns:
            DataFrame: Input data, rescaled for prioritization.
        """
        hc =int(prioritize.get('high_coeff', 1))
        mc =int(prioritize.get('med_coeff', 1))
        lc =int(prioritize.get('low_coeff', 1))
        if prioritize['high'] != "":
            df.loc[:,df.filter(regex=prioritize['high']).columns] = hc*df.loc[:,df.filter(regex=prioritize['high']).columns]
        if prioritize['med'] != "":
            df.loc[:,df.filter(regex=prioritize['med']).columns] = mc*df.loc[:,df.filter(regex=prioritize['med']).columns]
        if prioritize['low'] != "":
            df.loc[:,df.filter(regex=prioritize['low']).columns] = lc*df.loc[:,df.filter(regex=prioritize['low']).columns]
        return df

    
    def column_clean(self):
        """Complete data cleaning function.

        Returns:
            DataFrame: Numerical DataFrame for modeling.
            DataFrame: Clean DataFrame for calculating certain metrics and certain visualizations.
            dict: Dictionary containing data processing methods used.
            MinMaxScaler object.
        """
        # removing ignore
        df = self.data_raw.copy()
        df = df.drop(df.filter(regex=self.excl).columns, axis=1)
        to_drop = []
        for col in df.columns:
            try:
                df[col].nunique()
            except:
                to_drop.append(col)
            try:
                df[col] = df[col].astype(float)
            except:
                pass

        df = df.drop(to_drop, axis=1)

        # removing columns with 1 unique value
        df = df[df.columns[df.nunique() != 1]]

        # removing columns with more than 25% nulls
        df = df[df.columns[df.isna().sum() < df.shape[0]*0.25]]
        df_clean = df.copy()

        # identify object columns to process
        objs = df.select_dtypes(exclude=['int64', 'float64']).columns

        data_dict = {}
        to_dummy = []
        too_unique = []

        data_dict['categorical'] = {}

        for c in objs:
            keep, others = [], []
            # binary variables
            if df[c].nunique() == 2:
                zero, one = df[c].value_counts().index
                df[c] = df[c].apply(lambda v: 0 if v == zero else 1)
                data_dict['categorical'][c] = {zero: 0, one: 1}
            # to_dummy if fewer than 5 unique values
            elif 2 < df[c].nunique() <= 5:
                to_dummy.append(c)
                for k, v in df[c].value_counts().items():
                    if 'other' not in k:
                        keep.append((k, v))
                    else: 
                        others.append((k, v))
                    data_dict['categorical'][c] = {'kept': keep, 'others': others}

            # to_dummy, but changing values that take up less than 5% of values to "other"
            elif 5 < df[c].nunique() < df.shape[0]:
                for k, v in df[c].value_counts().items():
                    if v > df.shape[0]/20 and 'other' not in k:
                        keep.append((k, v))
                    else:
                        others.append((k, v))
                if keep != []:
                    to_dummy.append(c)
                    data_dict['categorical'][c] = {'kept': keep, 'others': others}
                    df[c] = df[c].apply(lambda v: 'other' if not any(v == x[0] for x in keep) else v)
                    df_clean[c] = df_clean[c].apply(lambda v: 'other' if not any(v == x[0] for x in keep) else v)
                else:
                    too_unique.append(c)

            # identifier columns (to drop for modeling)
            else:
                too_unique.append(c)

        data_dict['too_unique'] = too_unique

        # create dummy vars, scaling based on the number of unique values
        for d in to_dummy:
            df = df.join(pd.get_dummies(df[d], prefix=d)).drop(d, axis=1)

        df = df.set_index(self.user_id).drop([u for u in too_unique if u!=self.user_id], axis=1).dropna()
        df_clean = df_clean.set_index(self.user_id).drop([u for u in too_unique if u!=self.user_id], axis=1).dropna()

        # scale features for modeling
        scaler = MinMaxScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

        for d in to_dummy:
            c = df_scaled.filter(regex=f'^{d}').columns
            df_scaled[c] = df_scaled[c]/len(c)
        if self.semi_supervised!='no':
            df_scaled = self.prioritize_df(df_scaled, self.prioritize)
        
        self.data = df_scaled # numerical data
        self.data_clean = df_clean # cleaned data
        self.data_dict = data_dict 
        self.categorical_features = list(data_dict['categorical'].keys())
        self.continuous_features = [c for c in self.data_clean if c not in self.categorical_features]
        self.scaler = scaler
        
        
    def clean_check(self):
        # check if data has been cleaned
        if hasattr(self, 'data')==False or hasattr(self, 'data_clean')==False:
            print("Data has not been cleaned... Running self.column_clean() now.")
            self.column_clean()
        else:
            pass
        
        
    def score_k(self, plot=True):
        """Picking mathematically optimal number of clusters.

        Args:
            plot (bool, optional): Whether to output Plotly visualizations. Defaults to True.

        Returns:
            dict: Dictionary containing metrics across different cluster numbers.
        """
        if hasattr(self, 'k_min')==False or hasattr(self, 'k_max')==False:
            print("No min/max values of k set... Using default range of k=[2, 10]")
            k_range = range(2, 11)
            
        else:
            k_range = range(self.k_min, self.k_max+1)
        
        # check if data has been cleaned
        self.clean_check()
            
        if self.data.shape[0] >= 10000:
            data = self.data.sample(n=10000)
        else: 
            data = self.data

        wss = []
        sil = []
        for k in k_range:
            model = KMeans(n_clusters=k, random_state=0, n_init='auto').fit(data)
            wss.append(model.inertia_)
            sil.append(silhouette_score(data, model.labels_))

        # to determine best k
        elbow, dec, best_ind = 0, 0, 0
        for i, k in enumerate(k_range):
            diff = wss[i] - wss[i-1]
            if diff < dec:
                elbow = k
                dec = diff
                best_ind = i
                
        
        self.best_k = elbow
        if hasattr(self, 'k')==False:
            self.k = elbow
        self.wss_scores = wss
        self.sil_scores = sil
        self.k_range = k_range
        self.best_k_ind = best_ind

    
    def cluster(self):
        """Main clustering function that trains clustering model.

        Returns:
            DataFrame: Numerical cleaned data with cluster labels,
            DataFrame: Cleaned data with cluster labels,
            Trained model object.
        """
        
        # check if data has been cleaned
        self.clean_check()
            
        # check if a k-value has been determined
        if hasattr(self, 'k')==False:
            print("Number of clusters has not been defined, running k-search.")
            self.score_k(plot=False)
        
        if self.model_type!='faiss':
            model = KMeans(n_clusters=self.k, random_state=0, n_init='auto').fit(self.data)
            res = model.labels_
        else:
            d = self.data.values.copy(order='C').astype(np.float32)
            model = faiss.Kmeans(d=d.shape[1], k=self.k, niter=300, nredo=10)
            model.train(d)
            res = model.index.search(d, 1)[1].flatten()

        out, out_clean = self.data.copy(), self.data_clean.copy()
        out['cluster'] = res
        out_clean = out_clean.merge(out[['cluster']].reset_index(), left_index=True, right_on=self.user_id).set_index(self.user_id)

        out = Reducer().reduce(out, verbose=False)
        out_clean = Reducer().reduce(out_clean, verbose=False)
        
        self.data = out
        self.data_clean = out_clean
        self.model = model
        
    ##################################
    ### DATA & MODELING PARAMETERS ###
    ##################################
    
    def save_model(self):
        """Saving model parameters (centroids, scaler) to DataFrame.

        Args:
            model (obj): Trained model object.
            scaler (obj): Trained MinMaxScaler object.
            col_names (list): List of column names, for best results use cleaned numerical data's column names.
            semi_supervised (bool): Whether the model took in prioritized data.
            prioritize (dict): Prioritization features and coefficients.
            df (DataFrame): Numerical input data (binarized).
            transforms_df (DataFrame): DataFrame of column transforms.

        Returns:
            _type_: _description_
        """
        if self.fit_check==False:
            return None
        if hasattr(self, 'processing_df')==False:
            self.process_data_dict()

        col_names = self.data.drop('cluster',axis=1).columns
        vals = pd.DataFrame([self.scaler.scale_], columns=col_names, index=['scaler'])

        # additionally scale categorical variables (dividing values by number of unique vals)
        try: 
            dummies = self.processing_df.dropna(subset=['kept'])
            to_save = []
            for f in dummies.itertuples(index=False):
                if isinstance(f.kept, list):
                    unique = len(f.kept)
                else:
                    unique = len(f.kept.split(', '))
                to_save.append({'nunique': unique, 'cols': vals.filter(regex=f'^{f.feature}').columns, 'feat': f.feature})
                vals[vals.filter(regex=f'^{f.feature}').columns] = vals[vals.filter(regex=f'^{f.feature}').columns]/unique
        except: 
            pass

        if self.semi_supervised=='yes':
            vals = self.prioritize_df(vals, self.prioritize).T
        else:
            vals = vals.T

        try:
            centroid_df = pd.DataFrame(self.model.cluster_centers_, columns=col_names, 
                                       index=[f'cluster_{i}' for i in range(len(self.model.cluster_centers_))]).T
        except:
            centroid_df = self.data.groupby('cluster').mean().T
            centroid_df.columns = [f'cluster_{i}' for i in range(centroid_df.shape[1])]

        model_df = pd.concat([vals, centroid_df],axis=1).reset_index()
        model_df.columns = ['features'] + model_df.columns.tolist()[1:]
        
        self.centroids_scaler = model_df
    
        
    def fit_check(self):
        self.clean_check()
        if hasattr(self, 'model')==False:
            print('Model has not been fit. Run .cluster() to fit model.')
            return False
        
    def process_data_dict(self):
        """Function for processing data dictionary into DataFrame format for data cleaning reproduction.

        Returns:
            DataFrame: Table with data cleaning rules.
        """
        # check if data has been cleaned
        self.clean_check()

        if self.categorical_features == []:
            self.processing_df = pd.DataFrame([{'feature': 'no_categorical_features', 'type': 'continuous'}])
            return None 
        
        processing = []
        for k, v in self.data_dict.get('categorical', {}).items():
            out = {'feature': k}
            if list(v.values()) == [0, 1]:
                out['type'] = 'boolean'
                out['kept'] = None
                out['others'] = None
                for kk, vv in v.items():
                    if vv == 0:
                        out['zero'] = kk
                    elif vv == 1:
                        out['one'] = kk
            else:
                out['type'] = 'dummy'
                out['kept'] = [vv[0] for vv in v['kept']]
                out['others'] = [vv[0] for vv in v['others']]
                out['zero'] = None 
                out['one'] = None
            processing.append(out)
            
        self.processing_df = pd.DataFrame(processing)
        
    def get_histograms(self, n=50):
        
        if self.fit_check()==False:
            return None
        
        # continuous features
        clusts = list(self.cluster_freq.keys())
        if self.continuous_features==[]:
            out = pd.DataFrame.from_records([{'cluster': c, 'range': 0, 'freq': 0, 
                                              'feature': 'no_continuous_features', 'lower': 0, 'upper': 0} for c in clusts])
        else:
            histo = self.data_clean.copy()[self.continuous_features+['cluster']]

            for c in self.continuous_features:
                bins = n
                hist = pd.qcut(histo[c], n, duplicates='drop')
                while hist.nunique() == 1:
                    bins = bins + n
                    hist = pd.qcut(histo[c], bins, duplicates='drop')
                histo[c] = hist

            histos = []
            for c in self.continuous_features:
                h = histo.reset_index()[[c, 'cluster', self.user_id]].groupby(['cluster', c]).count().reset_index()
                h.columns = ['cluster', 'range', 'freq']
                h['feature'] = c
                histos.append(h)

            out = pd.concat(histos)
            out['lower'] = out['range'].map(lambda x: x.left)
            out['upper'] = out['range'].map(lambda x: x.right)

        # categorical features
        cat = self.categorical_features
        if cat == []:
            cats = pd.DataFrame.from_records([{'cluster': c, 'range': 0, 'freq': 0, 
                                              'feature': 'no_categorical_features', 'lower': 0, 'upper': 0} for c in clusts])
        else:
            cats = []
            for c in cat:
                ct = self.data_clean.reset_index()[[self.user_id, 'cluster', c]].groupby(['cluster', c]).count().reset_index()
                ct.columns = ['cluster', 'range', 'freq']
                ct['feature'] = c
                cats.append(ct)
            cats = pd.concat(cats)
        out = pd.concat([out, cats])

        self.histograms = out
        
        
    ##########################    
    ### CLUSTERING METRICS ###
    ##########################
    
    def clust_frequencies(self, plot=True):
        
        # check if model has been cleaned and fit
        if self.fit_check()==False:
            return None
        
        self.cluster_freq = self.data.cluster.value_counts().to_dict()

            
    @staticmethod
    def info_gain_calc(df, feature, label='cluster'):
        
        initial_vc = df[feature].value_counts(normalize=True)
        initial_ent = -(initial_vc * np.log(initial_vc)/np.log(np.e)).sum()

        gain = []

        for l in df[label].unique():
            vals = df[df[label]==l][feature]
            vc = vals.value_counts(normalize=True)
            prop = vals.shape[0] / df.shape[0]
            ent = -(vc * np.log(vc)/np.log(np.e)).sum()
            gain.append(prop*ent)

        return initial_ent - sum(gain)
    
        
    def clust_info_gain(self):
        
        if self.fit_check()==False:
            return None
        
        if self.categorical_features == []:
            self.info_gain = pd.DataFrame([('no_categorical_features', 1)], columns=['feature', 'impt'])
        else:
            information_gain = []
            for cat in self.categorical_features:
                information_gain.append((cat, self.info_gain_calc(self.data_clean, cat)))
            information_gain = sorted(information_gain, key=lambda x: x[1])
            self.info_gain = pd.DataFrame(information_gain, columns=['feature', 'impt'])
            
            
    def clust_rfc(self):

        if self.fit_check()==False:
            return None
        
        if self.continuous_features == []:
            clusts = list(self.cluster_freq.keys())
            self.rfc = pd.DataFrame([{'cluster': c, 'range': 0, 'freq': 0, 
                                    'feature': 'no_continuous_features', 'lower': 0, 
                                     'upper': 0} for c in clusts])
        else:
            rfc = []
            cont = self.data[self.continuous_features+['cluster']]
            rel_std = 1 - cont.groupby('cluster').std() / cont.drop('cluster', axis=1).std()
            for c in rel_std.index:
                t = pd.DataFrame(rel_std.loc[c,:]).reset_index()
                t.columns = ['feature', 'impt']
                t['cluster'] = c
                rfc.append(t)
            self.rfc = pd.concat(rfc).sort_values(['cluster', 'impt'])
            
    def clust_rf_impt(self):
        
        if self.fit_check()==False:
            return None
        
        X = self.data.drop('cluster', axis=1)
        y = self.data['cluster']
        model = RandomForestClassifier(n_estimators=50, max_depth=5)
        model.fit(X, y)
        
        fi = pd.DataFrame(X.columns, columns = ['feature'])
        fi['impt'] = model.feature_importances_
        
        self.rf_impt = fi
        self.rf_model = model
        
    def clust_shap(self, plot=False):
        
        if hasattr(self, 'rf_model')==False:
            self.clust_rf_impt()
            
        ss = []
        for c in self.data.cluster.unique():
            s = self.data[self.data.cluster==c].sample(min([2000, sum(self.data.cluster==c)]))
            ss.append(s)
        sample = pd.concat(ss)

        explainer = shap.Explainer(self.rf_model, sample)
        shap_values = explainer(sample, check_additivity=False)
        shaps = []
        X_c = pd.melt((sample > sample.median()).replace({True: 'high', False: 'low'}))
        for i in range(shap_values.shape[-1]):
            vals = shap_values.values[:,:,i]
            shap_df = pd.DataFrame(vals, columns=shap_values.feature_names)
            shap_df = pd.melt(shap_df)
            shap_df.columns = ['feature', 'shap_value']
            shap_df['cluster'] = i
            shap_df['feature_value'] = X_c['value']
            shaps.append(shap_df)
#             if plot==True:
#                 shap.plots.bar(shap_values[:,:,i])
#                 shap.plots.beeswarm(shap_values[:,:,i])
                
        shaps = pd.concat(shaps)
        shap_stats = shaps.groupby(by=["feature", "cluster", "feature_value"], 
                                   dropna=False, as_index=False).agg(['sum', 'count', 'mean'])
        shap_stats.columns = [item[0] + '_' + item[1] for item in shap_stats.columns]
        
        self.shap = shap_stats.reset_index()
            
            
    def combine_importances(self):
        
        if hasattr(self, 'cluster_freq')==False:
            print("Computing cluster frequencies...")
            self.clust_frequencies()
        if hasattr(self, 'info_gain')==False:
            print("Computing feature information gain...")
            self.clust_info_gain()
        if hasattr(self, 'rfc')==False:
            print("Computing cluster relative feature compactness...")
            self.clust_rfc()
        if hasattr(self, 'shap')==False:
            self.clust_rf_impt()
            print(("Computing Random Forest feature importances and SHAP values..."))
            
        i1 = pd.DataFrame([self.cluster_freq]).T.reset_index()
        i1.columns = ['cluster', 'impt']
        i1['kind'] = 'num'
        i1['feature'] = 'all'
        
        i2 = self.info_gain
        i2['cluster'] = -99
        i2['kind'] = 'info_gain'
        
        i3 = self.rfc
        i3['kind'] = 'feature_compactness'
        
        i4 = self.rf_impt
        i4['cluster'] = -99
        i4['kind'] = 'random_forest'
        
        impt_list = [i1, i2, i3, i4]
        
        if hasattr(self, 'wss_scores'):
            i5 = pd.DataFrame(self.wss_scores, columns=['impt'])
            i5['feature'] = self.k_range
            i5['cluster'] = -99
            i5['kind'] = 'wss'
            impt_list.append(i5)
        
        if hasattr(self, 'sil_scores'):
            i6 = pd.DataFrame(self.sil_scores, columns=['impt'])
            i6['feature'] = self.k_range
            i6['cluster'] = -99
            i6['kind'] = 'silhouette'
            impt_list.append(i6)
        
        impts = pd.concat(impt_list)
        impts['rnk'] = impts.groupby(["kind", "cluster"])["impt"].rank("dense", ascending=False)
        self.feature_importances = impts
        
        
    
    ###################
    ### PX PLOTTING ###
    ###################
    
    def plot_best_k(self):
        
        if hasattr(self, 'wss_scores')==False:
            print("Computing WSS and Silhouette for K values...")
            self.score_k()
            
        eval_k = make_subplots(rows=1, cols=2, 
                               subplot_titles=['Inertia / Within-Cluster Sum of Squares', 'Silhouette Scores'])

        wss_line = px.line(x=self.k_range, y=self.wss_scores)
        sil_line = px.line(x=self.k_range, y=self.sil_scores)

        wss_trace = [wss_line["data"][i] for i in range(len(wss_line["data"]))]
        sil_trace = [sil_line["data"][i] for i in range(len(sil_line["data"]))]

        for t in wss_trace:
            eval_k.append_trace(t, row=1, col=1)
        for t in sil_trace:
            eval_k.append_trace(t, row=1, col=2)

        for i in eval_k['layout']['annotations']:
            i['font'] = dict(size=13)

        eval_k.update_layout(height=400, width=800, 
                             title_text=f"Evaluating Best Number of Clusters: Best K = {self.best_k}", 
                             showlegend=False)
        eval_k.show()
        
    
    def plot_clust_frequencies(self):
        
        if hasattr(self, 'cluster_freq')==False:
            print("Computing cluster frequencies...")
            self.clust_frequencies()
        
        colors = px.colors.qualitative.Plotly[:len(self.cluster_freq)]
        pie = go.Figure(data=[go.Pie(values=list(self.cluster_freq.values()), 
                                     labels=list(self.cluster_freq.keys()))])
        pie.update_layout(title_text="Cluster Distribution of Customers", width=500, height=500)
        pie.update_traces(marker={'colors': colors})
        pie.show()
        
    def plot_info_gain(self):
        
        if hasattr(self, 'info_gain')==False:
            print("Computing feature information gain...")
            self.clust_info_gain()
        if self.categorical_features == []:
            print("No categorical features to compute Information Gain.")
            return None

        cat_gain = dict(self.info_gain)
        cat_bar = px.bar(x=self.info_gain.impt, y=self.info_gain.feature, 
           labels={'x': 'Information Gain', 'y': 'Feature'}, title="Categorical Important Features: By Information Gain")
        cat_bar.show()
        
    def plot_rfc(self):
        
        if hasattr(self, 'rfc')==False:
            print("Computing cluster relative feature compactness...")
            self.clust_rfc()
        if self.continuous_features == []:
            print("No continuous features to compute Relative Feature Compactness.")
            return None
        
        cl = self.rfc.cluster.unique().tolist()
        titles = [f'Cluster {c}' for c in cl]
        fig = make_subplots(rows=len(cl), cols=1, subplot_titles=titles, vertical_spacing = 0.1)
        colors = px.colors.qualitative.Plotly[:len(cl)]

        for c in range(len(cl)):
            cc = self.rfc[self.rfc.cluster==cl[c]].sort_values('impt')
            tr = px.bar(x=cc['impt'], y=cc['feature'],
                       range_x=[-1, 1], color_discrete_sequence=[colors[c]])
            traces = [tr['data'][t] for t in range(len(tr['data']))]
            for t in traces:
                fig.append_trace(t, row=c+1, col=1)

        fig.update_layout(height=350*len(cl), title_text="Per-Cluster Relative Feature Compactness", showlegend=False)
        fig.update_xaxes(range=[-1, 1])
        fig.show()
        
    def plot_rf_impt(self):

        fig = px.bar(self.rf_impt.sort_values('impt'), x='impt', y='feature', 
                     title='Overall Proportional Feature Importances', 
        labels={'impt': 'Proportional Importance', 'feature': 'Feature'})
        fig.show()
        
    def plot_shap(self):
        pass
    
    
    #########################
    ### SAVE TABLES TO TD ###
    #########################
    
    def save_tables(self, save=True):
        """Main function for saving tables to TD database.

        Returns (saves to sink_database):
            1. Data processing table with rules for categorical variables.
            2. Feature importances tables (excl SHAP values).
            3. SHAP values table.
            4. Final table with user IDs and cluster labels.
            5. Model table with parameters to scale new data.
            6. Histograms table for Treasure Insights dashboard.
        """
        
        if hasattr(self, 'processing_df')==False:
            self.process_data_dict()
        if hasattr(self, 'feature_importances')==False:
            self.combine_importances()
        if hasattr(self, 'shap')==False:
            self.clust_shap()
        if hasattr(self, 'centroids_scaler')==False:
            self.save_model()
        if hasattr(self, 'histograms')==False:
            self.get_histograms()
            
        final_table = self.data_clean[['cluster']].reset_index(drop=False)
        final_table['cluster_label'] = final_table['cluster'].map(lambda x: 'cluster_'+str(x))
        
        for t in [self.processing_df, self.feature_importances, self.shap, 
                  self.centroids_scaler, self.histograms, final_table]:
            t['session_id'] = self.session_id
            
        if save==True:
            print("Writing data processing table...")
            self.client.load_table_from_dataframe(self.processing_df, 'as_data_processing1', writer='bulk_import', if_exists='overwrite')
            print("Writing feature importances table...")
            self.client.load_table_from_dataframe(self.feature_importances, 'as_feature_importances_temp1', writer='bulk_import', if_exists='overwrite')
            print("Writing SHAP values table...")
            self.client.load_table_from_dataframe(self.shap, 'as_shap_temp1', writer='bulk_import', if_exists='overwrite')
            print("Writing final cluster labels table...")
            self.client.load_table_from_dataframe(final_table, 'final_cluster_table', writer='bulk_import', if_exists='overwrite')
            print("Writing model params table...")
            self.client.load_table_from_dataframe(self.centroids_scaler, 'as_model1', writer='bulk_import', if_exists='overwrite')
            print("Writing histograms table...")
            self.client.load_table_from_dataframe(self.histograms, 'as_histograms_temp1', writer='bulk_import', if_exists='overwrite')
        
