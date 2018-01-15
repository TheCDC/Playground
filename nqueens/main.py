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
    help="""Use the parallel version of the algorithm for significant speed gains.
This produces solutions out of order.""",
    default=False,
    action='store_true',
)


def main():
    args = parser.parse_args()
    N = args.N
    if args.multiprocess:
        algo = nqueens.generate_solutions_multiprocessed
    else:
        algo = nqueens.generate_solutions
    c = 0

    for s in algo(N):
        print(f"SOLUTION {c}")
        print(nqueens.render(s, N))
        c += 1
    # assert c == 92
    print(c)


if __name__ == '__main__':
    main()
