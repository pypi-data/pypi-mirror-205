# ml_autosegmentation

## Introduction

This Auto-segmentation solution aims to learn from customer data that lives in the CDP and cluster users based on specific characteristics (behaviors and attributes) to create actionable audiences that marketing teams can use for targeting and other business use cases.

This solution leverages traditional Machine Learning segmentation techniques, with the ability to adjust parameters to segment audiences with more marketing intuition, instead of fully relying on the ML formula.

The input of this solution can be any data that has a row-per-customer structure. It is suggested to run this on the customers table that is output from running the Master Segment, as most behavior tables would already be incorporated. Furthermore, if there are additional behaviors or attributes that are not part of the Master Segment, these tables should first be joined to the main customers table.


## Inputs

* `input_table`: the table to run Autosegmentation on. If multiple tables are to be used, they should already be joined prior to feeding it into this solution.

* `user_id`: the column containing the unique user IDs. Usually will be `td_canonical_id` or something similar. 

#### Optional Parameters

* `excl`: a list of features to exclude from Autosegmentation. The solution does have default filters (i.e. for time, training features and columns already titled "exclude")

* `priority_features`: a dictionary of features that the Autosegmentation will give heavier weightings to when creating segments. For example, if `rfm_tier` (recency, frequency, monetary) is given as a priority feature, clusters will be more divided based on the distribution of customers' RFM tier. Give a dictionary that has the format: 

```{'high': [], 'med': [], 'low': []}```

* `k`: the number of clusters, if you do not want to use the mathematically "optimal" number of clusters as defined by an ML formula. This can be used if you want a specific number of segments to be created from the audience. 

### Cluster, and Score Clusters

As we see, the optimal number of clusters is stored in the dictionary above. We can feed this value into our next function, that builds the final clustering/segmentation model. The `cluster` function here has two outputs:

1. The DataFrame with the final cluster numbers
2. The fit model object


## Outputs

### Visualizations

### Scoring K

This first function runs the clustering algorithm for a range of cluster numbers. This outputs a dictionary that has the numbers for plotting, as well as the `best_k`, to be fed into the next function.

The two line graphs show how two main metrics for determining best number of clusters change with the number of clusters.

#### Inertia (WSS)

Inertia measures the within-cluster sum of squares -- essentially how compact each cluster's points are. Naturally, the WSS will decrease with more clusters, so the line should be **monotonically decreasing**. What we're looking for here, is the "elbow" of the graph (therefore, sometimes this is referred to as the **elbow curve**) where the marginal decrease in WSS is most. The function automatically determines this.

#### Silhouette Score

This score measures the relative difference between points within a cluster to points outside a cluster, i.e. how "separated" the clusters are. The higher the score, the better. 

The "optimal" number of clusters shown by both metrics might not be the same, so model-builders are able to exercise some intuition and testing to see results from different numbers of clusters. 

#### Cluster distribution

A pie chart showing the number of customers in each segment.

#### Important features: categorical

A series of bar charts showing the distribution of an important feature across clusters. This is currently taking the features that have cluster purity in one or more clusters. i.e. Variable X in Cluster 1 only has the value 0.

#### Important features: continuous

To determine important features, a metric of **relative feature compactness** is used. This basically measures the relative standard deviation of a feature across each cluster and the entire input dataset. The intuition behind this, is if the standard deviation of a feature is much smaller in a single cluster compared to the population, that feature is more likely able to be used to characterize that cluster. 

For example, if CLTV (Customer Lifetime Value) is distributed fairly evenly from 0-100, it would have a relatively large standard deviation. If Cluster 1 has a CLTV range of 80-100, it would have a relatively lower standard deviation compared to the population, so CLTV might be a good descriptor of the cluster, i.e. Cluster 1 has customers with high lifetime value.

This data is shown in the form of distribution functions. The dotted line represents the distribution across the entire population, where the other filled lines represent the distribution of the feature within each cluster. More "important" features will show that the n clusters' lines look different from each other.

These numbers and features are all stored in the `output` dictionary, so plotting can be adjusted.

#### Visualizations

* Elbow curve & silhouette score to evaluate cluster quality at different numbers of clusters, also to check the relative quality of clusters compared to the "optimal" number of clusters selected by the solution

* Cluster distribution chart showing the number of customers in each cluster

* Distribution of important features across segments/clusters. This can help to explain the audience within each segment and drive marketing strategies for different groups.

### Additional steps

* This solution automatically turns categorical, non-numerical features into dummy variables, and scales them so their effect will not be blown up by the number of categories per feature

* Features are all normalized with a `MinMaxScaler` but can be changed in the future

## Additional Processes & Features

### Feature Engineering

Prior to modeling, this feature engineering function does several feature engineering steps:

1. Removes columns to be excluded from modeling. This includes `time`, features that are used as training features for other models, and any other columns input by the user to be excluded.

2. Identifies binary variables and turns them into dummy variables (more frequent value is always 0, less frequent is always 1)

3. Creates dummy variables, but only for values that are in more than 10% of rows. The rest are bucketed into an "other" category.

4. Removes identifier columns (names, emails, other ID columns), and turns the user-input ID column into the index.

5. Outputs the cleaned DataFrame, as well as a **data dictionary** that outlines which values have been turned into 0/1s for dummy variables, as well as which columns/values have been dropped. 

### Semi-supervised

The semi-supervised approach allows for certain features to be considered more than others. This is done by multiplying the feature by a factor after holistic scaling has been done. This is implemented in the `priority_features` input.


