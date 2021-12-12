import time

from LRSApp import LRSApp
from utlis.readFasta import Fasta


def main():
    fileName = "../files/testbsize.fasta"
    fasta = Fasta(fileName)

    index = 0
    for v in fasta.data.values():
        print(f"seq{index}")
        for i in range(2, 51):
            start = time.perf_counter()
            size = len(set(v))
            lrs = LRSApp(v, i * size * (size - 1))
            print(f"b Value: {i * size * (size - 1)}")
            lrs.runDPforLMSApp()
            end = time.perf_counter()
            max_score, tu, last_char, (x, y, z) = lrs.getTheBestScore()
            print(f"Input size: {len(v)}")
            print(f"Alphabet size: {lrs.l}")
            print(f"App score: {max_score}")
            print(f"Elapsed time: {end - start:0.4f} seconds")
            # lrs.printStack(lrs.backtracksol(x, y, z))
        index += 1


if __name__ == '__main__':
    main()
