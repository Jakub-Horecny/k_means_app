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

"""from File_Manager import FileManager
from Bayes import Bayes
path: str = "bayes2.xlsx"
manager = FileManager()
res: list = manager.load_data_xlsx(path)

for i in res:
    print(i)

bayes = Bayes()
bayes.count_bayes(path)"""

"""from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

from File_Manager import FileManager
import  numpy as np
from string import ascii_uppercase

data = list(range(65, 91))

file = FileManager()
X = file.load_data("test2.csv")
print(len(X))
letters: list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


#fig, axes = plt.subplots(1, 2, figsize=(8, 3))
#X = [[i] for i in [2, 8, 10, 4, 1, 9, 19, 0]]
Z = linkage(X, 'complete')
#fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z, labels=letters)
print(Z)
plt.show()"""

from matplotlib import pyplot as plt

from Clustering import Clustering

c = Clustering()
hierarchical, dn = c.hierarchical_clustering("test2.csv", False)
# print(hierarchical[:,2])
print(len(hierarchical)) # ok
print(max(hierarchical[:, 0:1]))

col1 = hierarchical[:, 0].tolist()
col2 = hierarchical[:, 1].tolist()

print(col1)
print(col2)

ascii_letters = 65
letters: list = list(range(ascii_letters, ascii_letters + len(hierarchical)))

for i, let in enumerate(letters):
    letters[i] = chr(let)

for i in range(len(hierarchical)):
    letters.append(chr(int(col1[i]) + ascii_letters) + chr(int(col2[i]) + ascii_letters))

s = max(hierarchical[:, 1])
temp_l = [""] * int(s)
print(temp_l)
plt.show()
