from typing import Tuple
from collections import Counter
import numpy as np
import copy
import statistics

from scipy import stats
from scipy.stats import norm

from File_Manager import FileManager


class Bayes:

    def __init__(self):
        self.file_manager = FileManager()

    def count_bayes(self, path: str) -> Tuple[list, list, list, list, list]:
        """
        implementované podľa Cvicenie-3-1.xlsx
        nie je to ideálne, ale čo sa dá robiť - ka si myslíš že to urobíš lepšie tak prosím...
        :return:
        :rtype: Tuple[list, list, list, list, list]
        :param path: cesta k súboru
        """
        matrix: list = self.file_manager.load_data_xlsx(path)
        unique_variable_list: list = []  # only unique values
        matrices_variable_count_list: list = []
        last: int = 0
        # vezme iba unikátne hodnoty z matice
        for variable in matrix:
            temp_indexes_list = variable[1:len(variable) - 1]  # odstráni prvý a posledný prvok
            temp_indexes_list = set(temp_indexes_list)  # vezme unikátne hodnoty
            temp_indexes_list = list(temp_indexes_list)  # pretypuje na list
            temp_indexes_list.sort()  # abecedne roztriedy
            unique_variable_list.append(temp_indexes_list)
            last = len(temp_indexes_list)

        # počet výskitu výsledkov
        # (Uver bude splateny) - koľko krát Ano/Nie
        # Cancer koľko krát - low/high
        # excel - 22Q
        quantity_of_results: list = copy.deepcopy((matrix[len(matrix) - 1])[1:len(matrix[0]) - 1])
        quantity_of_results.sort()
        counts: list = list(Counter(quantity_of_results).values())
        for i, c in enumerate(counts):
            counts[i] = c / len((matrix[0])[1:len(matrix[0]) - 1])  # prepočet na pravdepodobnosť výskytu

        # vytvorí nulové matice pre pomocné výpočty
        for variable in unique_variable_list:
            temp_matrix = np.zeros((len(variable), last))
            matrices_variable_count_list.append(temp_matrix)

        # deep copy pre
        probability_list: list = copy.deepcopy(matrices_variable_count_list)

        # print(temp_matrix)
        """print(unique_variable_list[0])
        print(unique_variable_list[0].index("no"))
        print(len(matrices_variable_count_list))
        print(len(matrix))"""

        # pocetnosti 3D matica
        # excel od A20
        for i, temp_matrix in enumerate(matrix):
            if i == len(matrix) - 1:
                break
            # print(i)
            matrix_m: list = (matrix[len(matrix) - 1])[1:len(temp_matrix) - 1]  # vezme všetko okrem prvého/ posledného
            temp_matrix: list = temp_matrix[1:len(temp_matrix) - 1]  # vezme všetko okrem prvého/ posledného
            # hladám indexi na pripočítanie hodnoty do pomocnej matice matrices_variable_count_list
            for j, temp_m in enumerate(temp_matrix):
                # pohiblivá premenná (Tumor, history..)
                temp_index1: int = unique_variable_list[i].index(temp_m)  # index 1
                # výsledok - (Uver bude splateny, Cancer...)
                temp_index2: int = unique_variable_list[len(matrix) - 1].index(matrix_m[j])  # index 2
                # pripočítanie výskytu
                matrices_variable_count_list[i][temp_index1][temp_index2] += 1
                # print(str(temp_val) + " " + str(temp_val2))

        # pravdepodobnosti
        # excel od A24
        for i, temp_matrix in enumerate(matrices_variable_count_list):
            for j, temp_matrix2 in enumerate(temp_matrix):
                for k, temp_matrix3 in enumerate(temp_matrix2):
                    delenec = temp_matrix3  # temp_matrix[k][j]
                    sum_ = sum(temp_matrix[:, k])  # vezme stĺpec
                    """print(len(temp_matrix))
                    print(temp_matrix[:, k])
                    print(delenec)"""

                    """temp_index: list = indexes_list[0]
                    indexes_list.pop(0)"""
                    t = delenec / sum_
                    probability_list[i][j][k] = t

        """for m in probability_list:
            print(m.tolist())"""

        # výpočet lingvistických hodônt - pravdepodobnosti
        linguistic: list = []
        for j, quantity_of_results in enumerate(unique_variable_list[len(unique_variable_list) - 1]):
            temp_list: list = []
            for i, m in enumerate(matrix):
                if i == len(matrix) - 1:
                    break

                value = m[len(m) - 1]
                # value2 = matrix[len(matrix) - 1][len(m)-1]
                value_index = unique_variable_list[i].index(value)
                temp_list.append(probability_list[i][value_index][j])
                """for j, quantity_of_results in enumerate(unique_variable_list[len(unique_variable_list) - 1]):
                    linguistic.append(probability_list[i][value_index][j])"""
                # value_index2 = unique_variable_list[len(unique_variable_list) - 1].index(value)
            linguistic.append(temp_list)

        # print(linguistic)
        # print(unique_variable_list[len(unique_variable_list) - 1])
        counts_result: list = [1] * len(linguistic)
        citatel: list = [1] * len(linguistic)
        for i, li in enumerate(linguistic):
            for j in li:
                citatel[i] = citatel[i] * j
            # pravdepodobnosť výskitu
            counts_result[i] = citatel[i] * counts[i]
        # print(citatel)

        counts_norm: list = [1] * len(linguistic)
        norm: list = [1] * len(linguistic)
        for i, (ci, res) in enumerate(zip(citatel, counts_result)):
            norm[i] = ci / sum(citatel)
            # pranásobené pravdepodobnosťou výsledku
            counts_norm[i] = res / sum(counts_result)
        # print(norm)

        return (list(unique_variable_list[len(unique_variable_list) - 1]),
                citatel, norm, counts_result, counts_norm)

    def count_bayes_numeric(self, path: str) -> Tuple[list, list, list, list]:
        """
        implementované podľa Cvicenie-3-1.xlsx
        :rtype: Tuple[list, list, list, list]
        :param path: cesta k xlsx suboru
        :return:
        """
        matrix: list = self.file_manager.load_data_xlsx(path)
        unique_variable_list: list = []  # only unique values
        matrices_variable_count_list: list = []
        last: int = 0
        numeric_values_index: int = 0
        # vezme iba unikátne hodnoty z matice
        for i, variable in enumerate(matrix):
            temp_indexes_list = variable[1:len(variable) - 1]  # odstráni prvý a posledný prvok
            if not (isinstance(temp_indexes_list[0], int) or isinstance(temp_indexes_list[0], float)):
                temp_indexes_list = set(temp_indexes_list)  # vezme unikátne hodnoty
                temp_indexes_list = list(temp_indexes_list)  # pretypuje na list
                temp_indexes_list.sort()  # abecedne roztriedy
                unique_variable_list.append(temp_indexes_list)
                last = len(temp_indexes_list)
            else:
                numeric_values_index = i

        # počet výskitu výsledkov
        # (Uver bude splateny) - koľko krát Ano/Nie
        # Cancer koľko krát - low/high
        # excel - 24Q
        quantity_of_results: list = copy.deepcopy((matrix[len(matrix) - 1])[1:len(matrix[0]) - 1])
        quantity_of_results.sort()
        counts: list = list(Counter(quantity_of_results).values())
        for i, c in enumerate(counts):
            counts[i] = c / len((matrix[0])[1:len(matrix[0]) - 1])  # prepočet na pravdepodobnosť výskytu

        # uložím riadok s numerickými hodnotami do samostatneho listu
        numeric_values_list: list = copy.deepcopy(matrix[numeric_values_index])
        # odstranim riadok s numerickimi hodnotami
        matrix.remove(matrix[numeric_values_index])

        # vytvorí nulové matice pre pomocné výpočty
        for variable in unique_variable_list:
            temp_matrix = np.zeros((len(variable), last))
            matrices_variable_count_list.append(temp_matrix)

        # deep copy pre
        probability_list: list = copy.deepcopy(matrices_variable_count_list)

        # pocetnosti 3D matica
        # excel od A24
        # okrem priemerov
        for i, temp_matrix in enumerate(matrix):
            if i == len(matrix) - 1:
                break
            # print(i)
            matrix_m: list = (matrix[len(matrix) - 1])[1:len(temp_matrix) - 1]  # vezme všetko okrem prvého/ posledného
            temp_matrix: list = temp_matrix[1:len(temp_matrix) - 1]  # vezme všetko okrem prvého/ posledného
            # hladám indexi na pripočítanie hodnoty do pomocnej matice matrices_variable_count_list
            for j, temp_m in enumerate(temp_matrix):
                # pohiblivá premenná (Tumor, history..)
                temp_index1: int = unique_variable_list[i].index(temp_m)  # index 1
                # výsledok - (Uver bude splateny, Cancer...)
                temp_index2: int = unique_variable_list[len(matrix) - 1].index(matrix_m[j])  # index 2
                # pripočítanie výskytu
                matrices_variable_count_list[i][temp_index1][temp_index2] += 1
                # print(str(temp_val) + " " + str(temp_val2))

        # pravdepodobnosti
        # excel od A24
        for i, temp_matrix in enumerate(matrices_variable_count_list):
            for j, temp_matrix2 in enumerate(temp_matrix):
                for k, temp_matrix3 in enumerate(temp_matrix2):
                    delenec = temp_matrix3  # temp_matrix[k][j]
                    sum_ = sum(temp_matrix[:, k])  # vezme stĺpec
                    t = delenec / sum_
                    probability_list[i][j][k] = t

        # vypocet priemeru a smerodajnej odchýliky
        # excel - 24N
        means_list: list = [0] * len(counts)
        stdev: list = [0] * len(counts)
        # vezme posledny s unique_variable_list
        for i, m in enumerate(unique_variable_list[len(unique_variable_list) - 1]):
            temp_count: int = 0
            temp_l: list = []
            for j, q in enumerate((matrix[len(matrix) - 1])[1:len(matrix[0]) - 1]):
                if m == q:
                    means_list[i] += numeric_values_list[j + 1]  # lebo prva hodnota je názov atribútu (VEK)
                    temp_l.append(numeric_values_list[j + 1])
                    temp_count += 1

            means_list[i] = means_list[i] / temp_count
            stdev[i] = statistics.stdev(temp_l)
        # print(means_list)
        # print(stdev)
        # print(counts)

        # vypočet normal_dist
        # excel - 33 C
        normal_dist_list: list = [0] * len(counts)
        for i, (s, m) in enumerate(zip(stdev, means_list)):
            normal_dist_list[i] = stats.norm.pdf(numeric_values_list[len(numeric_values_list) - 1], m, s)
        # print(normal_dist_list)

        # výpočet lingvistických hodnôt - pravdepodobnosti
        linguistic: list = []
        for j, quantity_of_results in enumerate(unique_variable_list[len(unique_variable_list) - 1]):
            temp_list: list = []
            for i, m in enumerate(matrix):
                if i == len(matrix) - 1:
                    break
                value = m[len(m) - 1]
                value_index = unique_variable_list[i].index(value)
                temp_list.append(probability_list[i][value_index][j])
            linguistic.append(temp_list)

        counts_result: list = [1] * len(linguistic)
        citatel: list = [1] * len(linguistic)
        for i, li in enumerate(linguistic):
            for j in li:
                citatel[i] = citatel[i] * j
            # pravdepodobnosť výskitu
            counts_result[i] = citatel[i] * counts[i] * normal_dist_list[i]
        # print(citatel)

        counts_norm: list = [1] * len(linguistic)
        norm: list = [1] * len(linguistic)
        for i, (ci, res) in enumerate(zip(citatel, counts_result)):
            norm[i] = ci / sum(citatel)
            # pranásobené pravdepodobnosťou výsledku
            counts_norm[i] = res / sum(counts_result)
        # print(norm)
        # print(counts_result)
        # print(counts_norm)

        return (list(unique_variable_list[len(unique_variable_list) - 1]),
                normal_dist_list, counts_result, counts_norm)
