import logging

import numpy as np

import XSet


class LRSApp():
    def __init__(self, s, b=None):
        self.s = s
        self.length = len(self.s)
        self.alph = None
        self.alph = self.alphabet()
        self.alphtoint = {}
        self.createalphtoint()
        self.l = len(self.alph)
        self.b = b if b is not None else 2 * self.l * (self.l - 1)
        self.Lsigma = None
        self.createauxilaryds()
        self.blockIndices = np.full(self.b, 0)
        self.createBlockIndices()
        self.tupletoInt = {}
        self.inttotuple = {}
        self.tuples = None
        self.createtupledatastructure()

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

        cs = self.numberofcharactersinarange(c, i, j)

        return cs

    def runDPforLMSApp(self):
        if self.length < self.b:
            raise Exception('Not enough string length to divide into ' + str(self.b) + ' blocks')
        else:
            self.DP = np.full((self.b, len(self.tuples), self.l), 0)
            # setting base conditions
            for sigma in range(self.l):
                self.DP[0][0][sigma] = 0
            for f in range(1, len(self.tuples)):
                for sigma in range(self.l):
                    # change in base condition
                    # if sigma \in F then we set DP[0][f][sigma] = 0
                    if self.alph[sigma] in self.tuples[f]:
                        self.DP[0][f][sigma] = 0
                    else:
                        self.DP[0][f][sigma] = -(self.length * self.length)

            # Filling the table
            negative_value = -self.length * self.length
            for i in range(1, self.b):
                for f in range(len(self.tuples)):
                    for sigma in range(self.l):
                        sigma_character = self.alph[sigma]
                        f_set = self.tuples[f]
                        if sigma_character not in f_set:
                            self.DP[i][f][sigma] = negative_value
                        # if sigma_character is in f_set
                        else:
                            case1_value = self.DP[i - 1][f][sigma] + self.getLsigma(sigma_character, i)
                            case2_value = negative_value
                            f_set_list = list(f_set)
                            f_set_list.remove(sigma_character)
                            f_prime_tuple = tuple(f_set_list)
                            f_prime_tuple_index = self.tupletoInt[f_prime_tuple]

                            # if f_set_list is empty we need to consider it as the empty set
                            if len(f_set_list) == 0:
                                case2_value = self.DP[i - 1][0][sigma] + self.getLsigma(sigma_character, i)

                            for sigma_prime in f_set_list:
                                sigma_prime_index = self.alphtoint[sigma_prime]
                                val = self.DP[i - 1][f_prime_tuple_index][sigma_prime_index] + self.getLsigma(
                                    sigma_character, i)
                                if val > case2_value:
                                    case2_value = val
                            # put the max value out of the case 1 and case 2
                            max_val = max(case1_value, case2_value)
                            self.DP[i][f][sigma] = max_val

    def createtupledatastructure(self):
        x = XSet.Xset(self.alph)
        self.tuples = x.powersetWithEmptySet()
        for i in range(len(self.tuples)):
            self.tupletoInt[self.tuples[i]] = i
            self.inttotuple[i] = self.tuples[i]

    def createalphtoint(self):
        for i in range(len(self.alph)):
            self.alphtoint[self.alph[i]] = i


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
    print(x.inttotuple)
    print(x.tupletoInt)
    print(x.DP[0][0])
    print(x.DP[-1][-1])
    pass


if __name__ == '__main__':
    main()
