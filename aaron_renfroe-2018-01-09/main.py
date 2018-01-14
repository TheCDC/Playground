import random


def num_groups(l):
    c = 0
    state = 0
    for i in l:
        if state == 0:
            if i == 0:
                pass
            elif i == 1:
                state = 1
                c += 1
        elif state == 1:
            if i == 0:
                state = 0
            elif i == 1:
                pass
    return c


def steps_until_target_groups(order, target_groups):
    mask = [0 for i in order]
    for index, d in enumerate(order):
        mask[d - 1] = 1
        if num_groups(mask) >= target_groups:
            return index + 1
    raise ValueError("Target num. of groups never reached!")


def main():
    data = list(range(50))
    random.shuffle(data)
    mask = [0 for i in data]

    for d in data:
        mask[d - 1] = 1
        print(d, mask, num_groups(mask))
    print(steps_until_target_groups(data, 20))


if __name__ == '__main__':
    main()
