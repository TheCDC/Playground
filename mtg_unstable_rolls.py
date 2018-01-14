from itertools import product
from itertools import combinations


def ndice(n=2, sides=6):
    s = 0
    c = 0
    for faces in product(range(1, sides + 1), repeat=n):
        l = list(abs(a - b) for a, b in combinations(faces, 2))
        # print(l)
        s += sum(l) / len(l)
        c += 1
    return s / c

if __name__ == '__main__':
    print("=============")
    print(ndice(2, 6))
    print("=============")
    print(ndice(3, 6))
    print("=============")
    print(ndice(2, 7))
