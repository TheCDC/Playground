import multiprocessing


def generate_next_partials(partial=None, n=8):
    if partial is None:
        partial = list()
    if len(partial) < n:
        for i in range(n):
            p = partial + [i]
            if check_newest(p):
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


def check_newest(psol):
    y = len(psol) - 1
    x = psol[y]
    for y2 in range(y):
        x2 = psol[y2]
        xdif = x2 - x
        ydif = y2 - y
        if xdif == 0 or xdif == ydif or xdif == -ydif:
            return False
    return True


def is_final(l, n):
    return len(l) == n


def render(l, n):
    line = ['-'] * n
    out = list()
    for i in l:
        buf = line[:]
        buf[i] = 'x'
        out.append(' '.join(buf))
    out.append('=' * len(out[-1]))
    return '\n'.join(out)


def generate_solutions(n=8):
    N = n
    queue = list()
    # prefill
    for x in generate_next_partials(n=n):
        queue.append(x)
    while len(queue) > 0:
        x = queue.pop(0)
        if is_final(x, N):
            yield x
        else:
            for xx in generate_next_partials(x, N):
                queue.append(xx)


def worker(n, batch_size, inqueue, outqueue):
    """Multiprocessing worker."""
    internal_queue = list()
    while True:

        p = inqueue.pop()

        if p is None:
            # print("quitting")
            outqueue.put(None)
            return
        internal_queue.append(p)
        # ========== Batches ==========
        # perform a batch of iterations before returning results
        # to the main queue
        for _ in range(batch_size):
            if len(internal_queue) == 0:
                # print("break")
                break
            sub_partial = internal_queue.pop()
            if is_final(sub_partial, n):
                # print("found", sub_partial)
                outqueue.put(sub_partial)
                # print(p)
            else:
                for next_partial in generate_next_partials(sub_partial, n):
                    # print("put into queue:", x)
                    internal_queue.append(next_partial)

        for _ in range(len(internal_queue)):
            x = internal_queue.pop()
            inqueue.append(x)
        internal_queue = list()


def generate_solutions_multiprocessed(n=8, num_processes=8, batch_size=1000):
    num_workers = num_processes
    with multiprocessing.Manager() as manager:

        partials_queue = manager.list()
        solutions_queue = manager.Queue()
        # prefill
        for _ in range(num_workers):
            partials_queue.append(None)
        for x in generate_next_partials([], n):
            # print("filled in:", x)
            partials_queue.append(x)
        workers = []
        for _ in range(num_workers):
            w = multiprocessing.Process(
                target=worker,
                args=(n, batch_size, partials_queue, solutions_queue))
            workers.append(w)
        found_exits = 0
        for w in workers:
            w.start()
        while found_exits < num_workers:
            # print(test)
            s = solutions_queue.get()
            if s is None:
                found_exits += 1
            else:
                yield s
        # for w in workers:
        #     w.join()
