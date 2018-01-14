import random


class Group:

    def __init__(self, start, end):
        tt = (start, end)
        self.start = min(tt)
        self.end = max(tt)

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.end > other.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return f"Group({self.start},{self.end})"


def is_overlap(g1, g2):
    return (g1.start <= g2.start and g2.start <= g1.end) or (g1.start <= g2.end and g2.end <= g1.end)


def absorb_groups(l):
    out = []
    count = 0
    if len(l) > 1:
        for a, b in zip(l, l[1:] + [None]):
            if b is None:
                pass
                # out.append(a)
            elif is_overlap(a, b):
                ng = Group(min(a, b).start, max(a, b).end)
                # print(f"Overlap: {a} {b} => {ng}")
                out.append(ng)
                count += 1
            else:
                # print(f"No overlap: {a} {b}")
                out.append(a)
    else:
        out = l[:]
    return (sorted(out), count)


print(Group(1, 2) < Group(1, 4))
data = sorted(Group(*random.sample(range(10 * i, 10 * (i + 1)), 2))
              for i in range(10))
# data = [Group(1, 2), Group(3, 4), Group(5, 6)]
print(data)
print(absorb_groups(data))
c = 1
while c > 0:
    data, c = absorb_groups(data)
    print(c)
print(data)
