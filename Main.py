from Clustering import Clustering

clu = Clustering()

x = [[1, 1], [2, 1], [4, 3],
     [4, 5], [2, 4]]
c = [[1, 1], [2, 1]]

clu.k_means_clustering(x, c)
