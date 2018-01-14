import sys


def generate_next_partials(partial=None, n=8):
    if partial is None:
        partial = list()
    if len(partial) < n:
        for i in range(n):
            p = partial + [i]
            if is_valid(p):
                yield p


def is_valid(l):
    for a in range(len(l)):
        ai = l[a]
        for b in range(a + 1, len(l)):
            bi = l[b]
            # check diagonal and horizontal
            # difference between rows
            x = a - b
            # difference between columns
            y = ai - bi
            # do two comparisons instead of one with abs
            # for performance
            if y == x or y == -x or ai == bi:
                return False

    return True


def is_final(l, n):
    return len(l) == n


def render(l, n):
    edge = '=' * n
    line = ['#'] * n
    out = list()
    for i in l:
        buf = line[:]
        buf[i] = 'x'
        out.append(' '.join(buf))
    out.append(edge)
    return '\n'.join(out)


def generate_solutions(n=8):
    N = n
    queue = list()
    # prefill
    for x in generate_next_partials(n=n):
        queue.append(x)
    while len(queue) > 0:
        x = queue.pop()
        if is_final(x, N):
            yield x
        else:
            for xx in generate_next_partials(x, N):
                queue.append(xx)


def main():
    assert not is_valid([0, 1, 2, 3])
    assert not is_valid([0, 2, 5, 7, 6, 3, 1, 4])
    # assert is_valid([1, 2, 0], 4)
    N = int(sys.argv[1])
    c = 0
    for s in generate_solutions(N):
        # print(f"SOLUTION {c}")
        # print(render(s, N))
        c += 1
    # assert c == 92
    print(c)


if __name__ == '__main__':
    main()
