def fcn(P, preferences, forbiddens):
    total_sum = [0 for _ in xrange(P)]
    total_complain = 0
    best_solution = []
    for p in preferences:
        for i, option in enumerate(p):
            total_sum[i] += int(option)
    for s in total_sum:
        if s > len(preferences) / 2:
            best_solution.append('1')
            total_complain += len(preferences) - s
        else:
            best_solution.append('0')
            total_complain += s

    min_deviation = 999999999999999
    queue = [(''.join(best_solution), 0)]
    traversed = set(''.join(best_solution))
    while len(queue) > 0:
        # print queue
        elem, cur_deviation = queue.pop(0)
        if elem not in forbiddens:
            # print elem, cur_deviation
            min_deviation = min(min_deviation, cur_deviation)
            continue
        for i, ch in enumerate(elem):
            new_ch = '1' if ch == '0' else '0'
            new_deviation = abs(len(preferences)-2*total_sum[i])
            new_string = elem[:i]+new_ch+elem[i+1:]
            if new_string not in traversed:
                traversed.add(new_string)
                queue.append((new_string, cur_deviation+new_deviation))
    return total_complain + min_deviation

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    N, M, P= [int(s) for s in raw_input().split(" ")]
    preferences, forbiddens = [], set()
    for j in xrange(1, N + 1):
        preferences.append(raw_input())
    for j in xrange(1, M + 1):
        forbiddens.add(raw_input())
    print "Case #{}: {}".format(i, fcn(P, preferences, forbiddens))
    # check out .format's specification for more formatting options
