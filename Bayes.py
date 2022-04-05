from File_Manager import FileManager
import numpy as np


class Bayes:

    def __init__(self):
        self.file_manager = FileManager()

    def count_bayes(self, path: str) -> None:
        """

        :rtype: None
        :param path: cesta k súboru
        """
        matrix: list = self.file_manager.load_data_xlsx(path)
        variable_list: list = []
        matrices_list: list = []
        last: int = 0
        for variable in matrix:
            temp = variable[1:len(variable)-1]
            temp = set(temp)
            temp = list(temp)
            variable_list.append(temp)
            last = len(temp)

        for variable in variable_list:
            temp_matrix = np.zeros((len(variable), last))
            print(temp_matrix)

