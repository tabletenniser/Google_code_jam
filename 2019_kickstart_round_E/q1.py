def fcn(As, K):
    As.sort()
    result = 0
    day = 1
    i = 0
    cur_quota = K
    while i < len(As):
        if cur_quota == 0:
            cur_quota = K
            day += 1
        if As[i] >= day:
            result += 1
            cur_quota -= 1
        i += 1
    return result

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
  N, K = [int(s) for s in raw_input().split(" ")]
  As = [int(s) for s in raw_input().split(" ")]
  print "Case #{}: {}".format(i, fcn(As, K))
  # check out .format's specification for more formatting options
