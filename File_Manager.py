
class FileManager:

    def load_data(self, path: str):
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