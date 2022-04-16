from typing import Tuple, Any

from sklearn.cluster import KMeans
import numpy as np

from scipy.cluster.hierarchy import dendrogram, linkage


from File_Manager import FileManager


class Clustering:

    def __init__(self):
        self.file_manager = FileManager()

    def hierarchical_clustering(self, path: str, clustering_type: bool) -> Tuple[Any, dict, Any, Any]:
        """
        vykoná hierarchické zhlukvoanie
        :rtype: Tuple[Any, dict, Any, Any]
        :param path: cesta k súboru
        :param clustering_type: o aký typ zhlukovania ide True -> single / False -> complete
        :return: výsledky, dendogram
        """
        data = self.file_manager.load_data(path)
        ascii_letters = list(range(65, 91)) # velké písmená v ascii tabulke - A, B, C..

        if len(data) <= len(ascii_letters):
            letters = ascii_letters[:len(data)]
            for i, let in enumerate(letters):
                letters[i] = chr(let)  # zmena cisla na písmeno
        else:
            letters = list(range(1, len(data)))  # ak je dát viac ako písmen, ostanú čísla

        # typ zhlukovania
        if clustering_type:
            hierarchical = linkage(data, 'single', optimal_ordering=True)
        else:
            hierarchical = linkage(data, 'complete', optimal_ordering=True)

        # fig = plt.figure(figsize=(25, 10))
        dn: dict = dendrogram(hierarchical, labels=letters)

        l_1, l_2 = self.__adjust_result(hierarchical, letters)

        #print(hierarchical[:, 2])
        return hierarchical[:, 2].tolist(), dn, l_1, l_2
        #return hierarchical.tolist(), dn
        #plt.show()

    def __adjust_result(self, hierarchical: object, letters: list) -> Tuple[list, list]:
        """
        zmení číselné hodnoty na písmená
        :param hierarchical: výsledok zierarchického zhlukovania
        :param letters: pole písmen
        :return:
        """
        col1 = hierarchical[:, 0].tolist()
        col2 = hierarchical[:, 1].tolist()
        l_1: list = []
        l_2: list = []

        for (c_1, c_2) in zip(col1, col2):
            letter_1 = letters[int(c_1)]
            letter_2 = letters[int(c_2)]
            l_1.append(letter_1)
            l_2.append(letter_2)
            letters.append(str(letter_1) + str(letter_2))
        return l_1, l_2

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
