from LRSApp import LRSApp
from utlis.readFasta import Fasta
import time


def main():
    fileName = "../files/teststringsize2.fasta"
    fasta = Fasta(fileName)
    for v in fasta.data.values():
        start = time.perf_counter()
        lrs = LRSApp(v)
        lrs.runDPforLMSApp()
        end = time.perf_counter()
        max_score, tu, last_char, (x, y, z) = lrs.getTheBestScore()
        print(f"Input size: {len(v)}")
        print(f"Alphabet size: {lrs.l}")
        print(f"App score: {max_score}")
        print(f"Elapsed time: {end - start:0.4f} seconds")
        # lrs.printStack(lrs.backtracksol(x, y, z))


if __name__ == '__main__':
    main()
