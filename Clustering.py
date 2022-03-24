from sklearn.cluster import KMeans
import numpy as np


class Clustering:

    def __init__(self):
        print()

    def k_means_clustering(self, data: list, centroid: list):
        data_np = np.array(data)
        centroid_np = np.array(centroid)

        kmeans = KMeans(n_clusters=2, random_state=0, init=c).fit(X)
        print(kmeans.labels_)
        # kmeans.predict([[1,1], [2,1]])
        print(kmeans.cluster_centers_)

        return kmeans.labels_, kmeans.cluster_centers_
