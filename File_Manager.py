class FileManager:

    def load_data(self, path: str) -> list:
        """
        načíta dáta z csv súboru
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
