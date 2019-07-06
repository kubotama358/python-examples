class Csv:
    def __init__(self, file_path):
        self.file = open(file_path, 'a')

    def write(self, data):
        self.file.write(data)
