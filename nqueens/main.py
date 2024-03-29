import sys
import nqueens
import argparse

parser = argparse.ArgumentParser("Generate solutions to the N-Queens problem.")

parser.add_argument(
    'N',
    metavar='N',
    type=int,
    help='The value of N for N-Queens. Board size and number of queens.',
)

parser.add_argument(
    '-m',
    '--multiprocess',
    default=False,
    help="""Enable multiprocessing.
    Use the parallel version of the algorithm for significant speed gains.
    This produces solutions out of order.""",
    action='store_true',
)

parser.add_argument(
    '-p',
    '--processes',
    help='Number of processes to execute in parallel.',
    default=8,
    type=int,
    metavar='processes',
)

parser.add_argument(
    '-b',
    '--batch-size',
    help='Size of iteration batches for processes..',
    default=10000,
    type=int,
    metavar='batch_size',
)

parser.add_argument(
    '-q',
    '--quiet',
    help="Suppress all output except the finaly tally.",
    default=False,
    action="store_true",
)

parser.add_argument(
    '-v',
    '--verbose',
    help="Render each solution as ASCII",
    default=False,
    action="store_true",
)


def wrapper(multi, n, nprocesses, batch):
    if multi:
        def wrapped():
            yield from nqueens.generate_solutions_multiprocessed(
                n=n,
                num_processes=nprocesses,
                batch_size=batch
            )
    else:
        def wrapped():
            yield from nqueens.generate_solutions(n=n)
    return wrapped


def main():
    args = parser.parse_args()
    N = args.N
    # print(vars(args))
    # quit()
    algo = wrapper(args.multiprocess, N, args.processes, args.batch_size)
    c = 0
    for s in algo():
        if not args.quiet:
            print(f"{c}")
            if args.verbose:
                print(nqueens.render(s, N))
        c += 1
    print(c)


if __name__ == '__main__':
    main()
