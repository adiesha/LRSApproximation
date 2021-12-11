from LRSApp import LRSApp
from utlis.readFasta import Fasta


def main():
    fileName = "files/test2.fasta"
    fasta = Fasta(fileName)
    for v in fasta.data.values():
        lrs = LRSApp(v)
        lrs.runDPforLMSApp()
        max_score, tu, last_char, (x, y, z) = lrs.getTheBestScore()
        print(max_score)
        lrs.printStack(lrs.backtracksol(x, y, z))


if __name__ == '__main__':
    main()
