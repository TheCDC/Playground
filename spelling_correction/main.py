from collections import Counter
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    'word',
    metavar='word',
    help='The possibly misspelled word to be checked.'
)


def total(c):
    return sum(abs(v)**2 for v in c.values())


def extract(word):
    c = Counter()
    for slice_length in range(1, 1 + 1):
        c.update([word[i:i + slice_length] for i in range(len(word))])
    return c


def distance(word, target):
    new_c = Counter(word.lower())
    new_c.subtract(target.lower())
    return total(new_c)


def check(word):
    out = []
    for good in words:
        if good.lower().startswith(word[0]):

            out.append((good, distance(word, good)))
    return sorted(out, key=lambda t: t[1])


words = []
with open('american-english') as f:
    for w in f:
        words.append(w.strip())
counts = [extract(w.lower()) for w in words]


def main():
    args = parser.parse_args()
    print("Word:", args.word)
    print(extract(args.word))
    print(check(args.word.lower())[:10])


if __name__ == '__main__':
    main()
