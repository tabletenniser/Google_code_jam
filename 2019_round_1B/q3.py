from __future__ import print_function
import sys

t = int(raw_input())  # read a line with a single integer
# print("Test cases: {}".format(t), file=sys.stderr)
for i in xrange(1, t + 1):
    a = int(raw_input())  # read a line with a single integer
    # print("A: {}".format(a), file=sys.stderr)
    grid = [['0' for _ in xrange(5)] for _ in xrange(100)]
    # index = 0
    col = 2
    while True:
        # col = (index % 23) * 3 + 2
        # index += 1
        print("2 {}".format(col))
        sys.stdout.flush()
        i,j = [int(s) for s in raw_input().split(" ")]
        if i == 0 and j == 0:
            break
        if i == -1 and j == -1:
            print("GRID:", file=sys.stderr)
            for row in grid:
                print(" ".join(row), file=sys.stderr)
            sys.exit(0)
        grid[j][i] = '1'
        if grid[col-1][1] == '1' and grid[col-1][2] == '1' and grid[col-1][3] == '1':
            col += 1
        # print("2 {} ==> {} {}".format(col, i, j), file=sys.stderr)
        # sys.stderr.flush()
