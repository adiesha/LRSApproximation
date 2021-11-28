import XSet


def main():
    alp = alphabet("122314")
    xset = XSet.Xset(alp)
    b = xset.powersetWithEmptySet()
    print(b)
    print(type(b[1]))
    print(tuple('2'))
    print(('2', '3') == ('3', '2'))


def powerset(alp):
    pass


def alphabet(a):
    alp = sorted(set(list(a)))
    print(alp)
    return alp


if __name__ == '__main__':
    main()
