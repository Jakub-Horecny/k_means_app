"""from Clustering import Clustering
clu = Clustering()

x = [[1, 1], [2, 1], [4, 3],
     [4, 5], [2, 4]]

c = [[1, 1], [2, 1]]

cc = "0,1,2"
path: str = "test2.csv"

labels, centers = clu.k_means_clustering(path, cc)
labels = labels.tolist()
centers = centers.tolist()
print(labels)
print(centers)"""

from File_Manager import FileManager
from Bayes import Bayes
path: str = "cv6.xlsx"
"""manager = FileManager()
res: list = manager.load_data_xlsx(path)

for i in res:
    print(i)"""

bayes = Bayes()
bayes.count_bayes(path)
