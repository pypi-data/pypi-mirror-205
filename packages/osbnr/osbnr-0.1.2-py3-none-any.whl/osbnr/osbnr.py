
# -*- coding: utf-8 -*-
#
# Author: Salma EL HAJJAMI
#
# OSBNR 

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

class OSBNR:
    def __init__(self, k=5):
        self.k = k # Number of clusters for k-means algorithm
        
    def fit_resample(self, X, y):
        minority_class_indices = np.where(y == 1)[0]
        majority_class_indices = np.where(y == 0)[0]
        
        # Step 2: Clustering
        kmeans = KMeans(n_clusters=self.k, random_state=0)
        X_minority = X[minority_class_indices]
        kmeans.fit(X_minority)
        
        # Step 3: Noise removal
        for i in range(self.k):
            # Calculate the distance from the farthest point in the minority class cluster to its center
            d_max_i = np.max(euclidean_distances(X_minority[kmeans.labels_ == i], [kmeans.cluster_centers_[i]], squared=True))
            
            # Calculate the distances from the majority class points to the centers of the minority class clusters
            d_maj_ij = euclidean_distances(X[majority_class_indices], [kmeans.cluster_centers_[i]], squared=True)
            
            # Remove noisy majority class points that fall within the cluster boundary of a minority class cluster
            noisy_indices = majority_class_indices[np.where(d_max_i >= d_maj_ij)[0]]
            majority_class_indices = np.setdiff1d(majority_class_indices, noisy_indices)
        
        # Step 4: Combine minority and reduced majority class points
        X_resampled = np.vstack((X[minority_class_indices], X[majority_class_indices]))
        y_resampled = np.hstack((y[minority_class_indices], y[majority_class_indices]))
        
        return X_resampled, y_resampled
