import functools
import multiprocessing
import os
import time


@functools.lru_cache(maxsize=None)
def is_prime(num):
    if num == 2:
        return True
    if num % 2 == 0 or num < 0:
        return False
    check = 3
    while check * check <= num:
        if num % check == 0:
            return False
        check += 2
    return True


def f(targs):
    """Solution is setup in this slightly ugly way since it
    was modified on a whim to support multiprocessing"""
    # Even values for b always produce a score of 0, so
    # we only check odds.
    a, bmax = targs
    best_a, best_b = None, None
    best = -1
    for b in range(1, bmax, 2):
        n = 0
        test = b
        while is_prime(test):
            n += 1
            test = (n * n) + (a * n) + b
        if n > best:
            best = n
            best_b = b
    return a, best_b, best


def g(targs):
    """Hopefully shortcutted version of f"""
    a, bmax = targs
    bs = primes_up_to(bmax)
    best_a, best_b = None, None
    best = -1
    for b in bs:
        n = 0
        test = b
        while is_prime(test):
            n += 1
            test = (n * n) + (a * n) + b
        if n > best:
            best = n
            best_b = b
    return a, best_b, best


@functools.lru_cache(maxsize=None)
def primes_up_to(pmax):
    print('Thread generating primes lower than {}...'.format(pmax))
    t = tuple([2] + [n for n in range(1, pmax, 2) if is_prime(n)])
    print('Thread found {} primes.'.format(len(t)))
    return t


def main(xmin, xmax, ymax):
    threads = os.cpu_count()
    print('Detected {} virtual CPUs, running with {} threads...\n'.format(
        threads, threads))
    # pool = multiprocessing.Pool(threads)
    # print('Pregenerating primes up {}...'.format(ymax))
    # unfiltered_primes = pool.map(filter_primes_multi, range(1, ymax, 2))
    # primes = [prime for prime in unfiltered_primes if prime != None]
    # primes.append(2)
    # print('Found {} primes.'.format(len(primes)))
    # print('Testing quadratics...')
    xs = range(xmin, xmax)
    ymaxes = [ymax] * (xmax - xmin)
    # m = pool.map(g, zip(xs, ymaxes))
    m = map(g, zip(xs, ymaxes))
    # m = [g()]
    vals = max(m, key=lambda x: x[2])
    print('Done!')
    print('n^2 + {}n + {} produced {} consecutive primes.'.format(*vals))

if __name__ == '__main__':
    start = time.time()
    a, b, c = -10000, 10000, 10001
    print('Running for a between {} and {}, b up to {}...'.format(a, b, c))
    main(a, b, c)
    finish = time.time()
    print('Ran in {0:.3g}s in real time. Measured by start and stop time.'.format(
        finish - start))
