from typing import Tuple

from sklearn.cluster import KMeans
import numpy as np

from scipy.cluster.hierarchy import dendrogram, linkage


from File_Manager import FileManager


class Clustering:

    def __init__(self):
        self.file_manager = FileManager()

    def hierarchical_clustering(self, path: str, clustering_type: bool) -> Tuple[list, dict]:
        """
        vykoná hierarchické zhlukvoanie
        :rtype: Tuple[list, dict]
        :param path: cesta k súboru
        :param clustering_type: o aký typ zhlukovania ide True -> single / False -> complete
        :return: výsledky, dendogram
        """
        data = self.file_manager.load_data(path)
        ascii_letters = list(range(65, 91))

        if len(data) <= len(ascii_letters):
            letters = ascii_letters[:len(data)]
            for i, let in enumerate(letters):
                letters[i] = chr(let)
        else:
            letters = list(range(1, len(data)))

        # typ zhlukovania
        if clustering_type:
            hierarchical = linkage(data, 'single', optimal_ordering=True)
        else:
            hierarchical = linkage(data, 'complete', optimal_ordering=True)

        # fig = plt.figure(figsize=(25, 10))
        dn: dict = dendrogram(hierarchical, labels=letters)
        print(hierarchical[:, 2])
        return hierarchical.tolist(), dn
        #plt.show()

    def k_means_clustering(self, path: str, centroids: str) -> tuple:
        """
        vykoná k means zhlukovanie
        :param path: cesta k súboru
        :param centroids: zadané body, ktoré reprezentujú centroid
        :return: priradenie bodov do zhlukov, súradnice stredov
        :rtype: tuple
        """
        data: list = self.file_manager.load_data(path)
        centroids_id: list = self.__adjust_centroids(centroids)

        centroids_list: list = []
        for cent in centroids_id:
            # ak by dal ako vstup hodnoty 0 a menej
            if (cent - 1) < 0:
                raise IndexError

            centroids_list.append(data[cent - 1])

        data_np = np.array(data)
        centroids_list_np = np.array(centroids_list)

        kmeans = KMeans(n_clusters=len(centroids_list), random_state=0, init=centroids_list_np).fit(data_np)
        # print(kmeans.labels_)
        # kmeans.predict([[1,1], [2,1]])
        # print(kmeans.cluster_centers_)
        temp_labels = kmeans.labels_.tolist()
        for i in range(len(temp_labels)):
            temp_labels[i] = temp_labels[i] + 1

        return temp_labels, kmeans.cluster_centers_.tolist()

    def __adjust_centroids(self, centroids: str) -> list:
        """
        upraví input od používateľa
        :param centroids:
        :return: indexi bodov, ktoré budú použité ako počiatočné centroidy
        :rtype: list
        """
        c: list = centroids.split(",")
        c = list(map(int, c))
        return c
