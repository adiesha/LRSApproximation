def main():
    fasta = Fasta("../test.fasta")
    print(fasta.data)


class Fasta:

    def __init__(self, filename):
        self.fileName = filename
        self.data = {}
        self.file = None
        self.lines = None
        self.read()

    def read(self):
        self.file = open(self.fileName, 'r')
        self.lines = self.file.readlines()
        index = None
        for line in self.lines:
            if line.startswith(">"):
                index = int(line.split("seq")[-1])
            else:
                self.data[index] = line.rstrip()

    def getData(self):
        return self.data


if __name__ == '__main__':
    main()
