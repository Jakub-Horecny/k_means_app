import xlrd


class FileManager:

    def __init__(self):
        self.row_default = 0
        self.column_default = 1

    def load_data(self, path: str) -> list:
        """
        načíta dáta z csv/txt súboru
        :rtype: list
        :param path: cesta k súboru
        :return: matica súradníc
        """
        results: list = []
        with open(path, "r") as file:
            while True:
                line = file.readline().strip()
                if not line:
                    break
                entry: list = line.split(",")
                entry = list(map(float, entry))
                results.append(entry)
        return results

    def load_data_xlsx(self, path: str) -> list:
        """
        načíta dáta z xlsx súboru
        :rtype: list
        :param path: cesta k súboru
        :return: matica hodnôt
        """
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)

        row = self.row_default
        col = self.column_default

        result_matrix: list = []
        temp_list: list = []
        while True:
            cell = sheet.cell(row, col)
            if cell.value == "":
                row = self.row_default
                col += 1
                # kontrola či je v ďaľšom stĺpci hodnota, ak nie koniec
                cell = sheet.cell(row, col)
                if cell.value == "":
                    result_matrix.append(temp_list)
                    break
                else:
                    result_matrix.append(temp_list)
                    temp_list = []
                    continue
            row += 1
            temp_list.append(cell.value)

        return result_matrix
