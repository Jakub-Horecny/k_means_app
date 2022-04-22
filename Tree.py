import json
from typing import Tuple, Union, Any

import pandas as pd  # for manipulating the csv data
import numpy as np  # for mathematical calculation

"""
zdroj
https://medium.com/geekculture/step-by-step-decision-tree-id3-algorithm-from-scratch-in-python-no-fancy-library-4822bbfdd88f
"""


class Tree:

    def __init__(self):
        self.important: list = []
        self.total_entr_l: list = []
        self.entropy_l: list = []
        self.information: list = []

    def calc_total_entropy(self, train_data, label: str, class_list) -> float:
        """

        :param train_data:
        :param label:
        :param class_list:
        :return:
        """
        total_row = train_data.shape[0]  # the total size of the dataset
        total_entr: float = 0

        for c in class_list:  # for each class in the label
            total_class_count = train_data[train_data[label] == c].shape[0]  # number of the class
            if total_class_count == 0:
                total_class_entr: float = 0
            else:
                total_class_entr: float = - (total_class_count / total_row) * np.log2(
                    total_class_count / total_row)  # entropy of the class
            # kvôli tomu že ten kokotko sem nedal túto podmienku som dostal FX áááááááááááááááááááááááááá
            """if np.isnan(total_class_entr):
                total_class_entr = 0
                print(total_class_count)
                print(total_row)"""
            # iba tieto dva pojebané riadky
            total_entr += total_class_entr  # adding the class entropy to the total entropy of the dataset

        self.total_entr_l.append(total_entr)
        return total_entr

    def calc_entropy(self, feature_value_data, label: str, class_list: list) -> float:
        """

        :param feature_value_data:
        :param label:
        :param class_list:
        :return:
        """
        class_count = feature_value_data.shape[0]
        entropy: float = 0

        for c in class_list:
            label_class_count = feature_value_data[feature_value_data[label] == c].shape[0]  # row count of class c
            entropy_class: float = 0
            if label_class_count != 0:
                probability_class = label_class_count / class_count  # probability of the class
                entropy_class = - probability_class * np.log2(probability_class)  # entropy
            entropy += entropy_class

        # entropy_l.append(entropy)
        return entropy

    def calc_info_gain(self, feature_name, train_data, label: str, class_list: list) -> float:
        """

        :param feature_name:
        :param train_data:
        :param label:
        :param class_list:
        :return:
        """
        feature_value_list = train_data[feature_name].unique()  # unqiue values of the feature
        total_row = train_data.shape[0]
        feature_info: float = 0.0

        for feature_value in feature_value_list:
            feature_value_data = train_data[
                train_data[feature_name] == feature_value]  # filtering rows with that feature_value
            feature_value_count = feature_value_data.shape[0]
            feature_value_entropy = self.calc_entropy(feature_value_data, label,
                                                      class_list)  # calculcating entropy for the feature value
            # print(feature_value_entropy)
            feature_value_probability: float = feature_value_count / total_row
            self.entropy_l.append([feature_name, feature_value, feature_value_probability * feature_value_entropy])
            feature_info += feature_value_probability * feature_value_entropy  # calculating information of the feature value

        return self.calc_total_entropy(train_data, label,
                                       class_list) - feature_info  # calculating information gain by subtracting

    def find_most_informative_feature(self, train_data, label: str, class_list: list) -> str:
        """

        :param train_data:
        :param label:
        :param class_list:
        :return:
        """
        feature_list = train_data.columns.drop(label)  # finding the feature names in the dataset
        # N.B. label is not a feature, so dropping it
        max_info_gain = -1
        max_info_feature: str = ""

        for feature in feature_list:  # for each feature in the dataset
            feature_info_gain = self.calc_info_gain(feature, train_data, label, class_list)
            if max_info_gain < feature_info_gain:  # selecting feature name with highest information gain
                max_info_gain = feature_info_gain
                max_info_feature = feature
        self.information.append(max_info_gain)
        # atribúti čo majú najväčší vpliv
        # max_info_feature_l.append(max_info_feature)
        self.important.append(max_info_feature)
        return max_info_feature

    def generate_sub_tree(self, feature_name: str, train_data, label: str, class_list: list) -> Tuple[dict, Any]:
        """

        :param feature_name:
        :param train_data:
        :param label:
        :param class_list:
        :return:
        """
        feature_value_count_dict = train_data[feature_name].value_counts(
            sort=False)  # dictionary of the count of unqiue feature value
        tree: dict = {}  # sub tree or node

        for feature_value, count in feature_value_count_dict.iteritems():
            feature_value_data = train_data[
                train_data[feature_name] == feature_value]  # dataset with only feature_name = feature_value

            assigned_to_node: bool = False  # flag for tracking feature_value is pure class or not
            for c in class_list:  # for each class
                class_count = feature_value_data[feature_value_data[label] == c].shape[0]  # count of class c

                if class_count == count:  # count of feature_value = count of class (pure class)
                    tree[feature_value] = c  # adding node to the tree
                    train_data = train_data[
                        train_data[feature_name] != feature_value]  # removing rows with feature_value
                    assigned_to_node = True
            if not assigned_to_node:  # not pure class
                tree[feature_value] = "?"  # should extend the node, so the branch is marked with ?

        return tree, train_data

    def make_tree(self, root: dict, prev_feature_value, train_data, label: str, class_list: list) -> None:
        """

        :param root:
        :param prev_feature_value:
        :param train_data:
        :param label:
        :param class_list:
        """
        if train_data.shape[0] != 0:  # if dataset becomes enpty after updating
            # hladam ktora trieda ma najvacsi prinos do buducna takye najvacsiu informaciu
            max_info_feature: str = self.find_most_informative_feature(train_data, label,
                                                                  class_list)  # most informative feature
            tree, train_data = self.generate_sub_tree(max_info_feature, train_data, label,
                                                      class_list)  # getting tree node and updated dataset

            if prev_feature_value is not None:  # add to intermediate node of the tree
                root[prev_feature_value] = dict()
                root[prev_feature_value][max_info_feature] = tree
                next_root = root[prev_feature_value][max_info_feature]
            else:  # add to root of the tree
                root[max_info_feature] = tree
                next_root = root[max_info_feature]

            for node, branch in list(next_root.items()):  # iterating the tree node
                if branch == "?":  # if it is expandable
                    feature_value_data = train_data[train_data[max_info_feature] == node]  # using the updated dataset
                    self.make_tree(next_root, node, feature_value_data, label,
                                   class_list)  # recursive call with updated dataset

    def id3(self, train_data_m, label: str) -> dict:
        """

        :param train_data_m:
        :param label:
        :return:
        """
        train_data = train_data_m.copy()  # getting a copy of the dataset
        tree: dict = {}  # tree which will be updated
        class_list: list = train_data[label].unique()  # getting unqiue classes of the label
        self.make_tree(tree, None, train_data_m, label, class_list)  # start calling recursion
        return tree

    def start(self, path: str, parameter: str) -> Tuple[dict, list, list, list]:
        """
        vykoná algoritmus ID3
        :param path: cesta k súboru
        :param parameter: rozhodujúci parameter
        :return:
        """
        train_data_m: Union = pd.read_csv(path)  # importing the dataset from the disk
        # print(train_data_m)
        tree: dict = self.id3(train_data_m, parameter)
        # prd = self.calc_info_gain('History', train_data_m, 'Cancer', ['high', 'low'])
        # print(prd)
        return tree, self.important, self.entropy_l, self.information

# t = Tree()
# tree, important = t.start("data3.csv", 'Sosovky')
# print(json.dumps(tree, indent=4))
# print(tree)
