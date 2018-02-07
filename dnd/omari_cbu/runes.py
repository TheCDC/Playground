import csv
from string import ascii_lowercase
from collections import Counter
english_vowels = set('aeiou')
english_consonants = set(ascii_lowercase) - english_vowels


class Rune:

    def __init__(self, char, name, concepts, schools):
        self.character = char
        self.name = name
        self.concepts = concepts
        self.schools = schools

    @classmethod
    def from_row(self, row):
        return Rune(
            row[0],
            row[1],
            [x.strip() for x in row[2].split(',')],
            [x.strip() for x in row[3].split(',')]
        )

    def __repr__(self):
        return str(vars(self))


class Spell:

    def __init__(self, runes):
        self.word = ''.join(rune.character for rune in runes)
        self.names = ', '.join(rune.name for rune in runes)
        self.concepts = ', '.join(rune.concept for rune in runes)
        c = Counter()
        for r in runes:
            c.update(r.schools)
        self.schools = c


with open('runes.csv') as f:
    rows = list(csv.reader(f, delimiter='|'))

runes = [Rune.from_row(r) for r in rows]

runic_vowels = {w[0] for w in rows if w[0][0].lower() in english_vowels}
runic_consonants = {w[0]
                    for w in rows if w[0][0].lower() in english_consonants}

rune_to_description = {r[0]: r for r in rows}
# print(rune_to_description)


def get_schools(row):
    return Counter(x.strip()
                   for x in row[3].strip().split(',') if len(x.strip()) > 0)


def generate_combinations():
    sorted_consonants = tuple(sorted(runic_consonants))
    sorted_vowels = tuple(sorted(runic_vowels))
    for a in sorted_consonants:
        for b in sorted_vowels:
            for c in sorted_consonants + sorted_vowels:
                if c != a and c != b:
                    yield [rune_to_description[x] for x in [a, b, c]]


def merge_rows(rs):
    t = list(zip(*rs))
    c = Counter()
    for r in rs:
        c.update(get_schools(r))
    c_str = ', '.join('{}={}'.format(k, v) for k, v in c.most_common(10))
    return [''.join(t[0]), ', '.join(t[1]), ', '.join(t[2]), c_str]
    # return [', '.join(i) for i in zip(*rs)]


total = 0
with open('runes_converted.csv', 'w') as f:
    writer = csv.writer(f)
    for comb in generate_combinations():
        total += 1
        writer.writerow(merge_rows(comb))

print('Num. Consonants:', len(runic_consonants))
print('Num. Vowels:', len(runic_vowels))
print('Num. Combinations:', total)
