from sklearn.cluster import KMeans
import numpy as np

from File_Manager import FileManager


class Clustering:

    def __init__(self):
        self.file_manager = FileManager()

    def k_means_clustering(self, path: str, centroids: str) -> tuple:
        """
        vykoná k means zhlukovanie
        :param path: cesta k súboru
        :param centroids: zadané body, ktoré reprezentujú centroid
        :return: priradenie bodov do zhlukov, súradnice stredov
        :rtype: tuple
        """
        data: list = self.file_manager.load_data(path)
        centroids_id: list = self.adjust_centroids(centroids)

        centroids_list: list = []
        for cent in centroids_id:
            centroids_list.append(data[cent])

        data_np = np.array(data)
        centroids_list_np = np.array(centroids_list)

        kmeans = KMeans(n_clusters=len(centroids_list), random_state=0, init=centroids_list_np).fit(data_np)
        # print(kmeans.labels_)
        # kmeans.predict([[1,1], [2,1]])
        # print(kmeans.cluster_centers_)

        return kmeans.labels_.tolist(), kmeans.cluster_centers_.tolist()

    def adjust_centroids(self, centroids: str) -> list:
        """
        upraví input od používateľa
        :param centroids:
        :return: indexi bodov, ktoré budú použité ako počiatočné centroidy
        :rtype: list
        """
        c: list = centroids.split(",")
        c = list(map(int, c))
        return c
