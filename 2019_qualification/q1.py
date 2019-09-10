def calculate_min_needed(levels, total_pow, d):
    result = 0
    while total_pow > d:
        last_pow = sorted(levels.keys())[-1]
        if last_pow == 1:
            return "IMPOSSIBLE"
        total_pow -= last_pow/2
        levels[last_pow] -= 1
        if levels[last_pow] == 0:
            del levels[last_pow]
        levels[last_pow/2] = levels.get(last_pow/2, 0) + 1
        result += 1

    return result

def fcn(d, p):
    cur_pow = 1
    total_pow = 0
    levels = dict()
    for ch in p:
        if ch == 'C':
            cur_pow *= 2
        elif ch == 'S':
            levels[cur_pow] = levels.get(cur_pow, 0) + 1
            total_pow += cur_pow
    result = calculate_min_needed(levels, total_pow, d)
    return result

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
  d, p = [s for s in raw_input().split(" ")]  # read a list of integers, 2 in this case
  d = int(d)
  print "Case #{}: {}".format(i, fcn(d, p))
  # check out .format's specification for more formatting options
