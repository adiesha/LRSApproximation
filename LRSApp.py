import logging

import numpy as np


class LRSApp():
    def __init__(self, s, b=None):
        self.s = s
        self.length = len(self.s)
        self.alph = None
        self.alph = self.alphabet()
        self.l = len(self.alph)
        self.b = b if b is not None else 2 * self.l * (self.l - 1)
        self.Lsigma = None
        self.createauxilaryds()
        self.blockIndices = np.full(self.b, 0)
        self.createBlockIndices()

    def alphabet(self):
        return self.alph if self.alph is not None else sorted(list(set(self.s)))

    def setb(self, b):
        l = len(self.alph)
        self.b = b if b is not None else 2 * l * (l - 1)

    def createauxilaryds(self):
        self.Lsigma = dict.fromkeys(self.alph)
        for k in self.Lsigma:
            self.Lsigma[k] = np.full(len(self.s), 0)

        i = 0
        for c in self.s:
            for k in self.Lsigma.keys():
                if k == c:
                    self.Lsigma[k][i] = self.Lsigma[k][i - 1 if i - 1 >= 0 else 0] + 1
                else:
                    self.Lsigma[k][i] = self.Lsigma[k][i - 1 if i - 1 >= 0 else 0]
            i += 1
        pass

    def numberofcharactersinarange(self, c, i, j):
        if i >= 0 and j < self.length:
            return self.Lsigma[c][j] - (0 if i < 1 else self.Lsigma[c][i - 1])

    def createBlockIndices(self):
        length = self.length
        nofb = self.b
        remainder = length % nofb
        blksize = length // nofb
        for i in range(nofb):
            extra = (1 if remainder > 0 else 0)
            beginning = -1 if i == 0 else self.blockIndices[i - 1]
            self.blockIndices[i] = beginning + extra + blksize
            remainder -= 1

    def getLsigma(self, c, blockNumber):
        if blockNumber < 1:
            logging.error("Block number start from 1")
            raise Exception("Block number start from 1")
        if blockNumber > self.b:
            logging.error("Block number out of bound")
            raise Exception("Block number out of bound")

        i = 0
        if blockNumber > 1:
            i = self.blockIndices[blockNumber - 2] + 1
        j = self.blockIndices[blockNumber - 1]
        print(i, j)
        cs = self.numberofcharactersinarange(c, i, j)
        print(cs)
        return cs

    def runDPforLMSApp(self):
        if self.length < self.b:
            raise Exception('Not enough string length to divide into ' + str(self.b) + ' blocks')


def main():
    x = LRSApp("aaaaaaaaaaaaaaaaattttaaaaaaavaaaaaaassssssssatttttttttaaaaaaaaaaaaatttttttttttttaaaaavvvvvv")
    print("Number of blocks " + str(x.b))
    print("Length of the string " + str(x.length))

    print(x.numberofcharactersinarange('a', 0, 2))
    print(x.numberofcharactersinarange('a', 1, 2))
    print(x.numberofcharactersinarange('a', 1, 3))
    print(x.numberofcharactersinarange('a', 4, 5))
    print(x.numberofcharactersinarange('a', 2, 5))
    print(x.numberofcharactersinarange('a', 1, 7))
    print(x.numberofcharactersinarange('a', 0, 7))
    print("----------------------------")
    print(x.blockIndices)
    print("----------------------------")
    print()
    x.getLsigma('a', 2)
    x.getLsigma('a', 1)
    x.getLsigma('a', 24)
    x.getLsigma('a', 23)
    x.getLsigma('a', 22)
    x.getLsigma('a', 5)
    x.getLsigma('a', 6)
    x.runDPforLMSApp()
    pass


if __name__ == '__main__':
    main()
