def fcn(As, K):
    prev_num = None
    last_num_occurance = dict()
    num_diff = 0
    abnormalities = {}
    for i, elem in enumerate(As):
        if prev_num and elem != prev_num:
            if elem in last_num_occurance:
                abnormalities[elem] = abnormalities.get(elem, []) + [i - last_num_occurance[elem]]
            num_diff += 1
        prev_num = elem
        last_num_occurance[elem] = i
    answer = num_diff - K
    # print answer, abnormalities
    real_answer = max(answer, 0)
    for key, value in abnormalities.items():
        cur_min_answer = max(answer, 0)
        ab_left = answer
        for val in sorted(value):
            if ab_left > val:
                cur_min_answer -= 1
                ab_left -= val
        real_answer = min(real_answer, cur_min_answer)
    return real_answer

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
  _, K = [int(s) for s in raw_input().split(" ")]
  As = [int(s) for s in raw_input().split(" ")]
  print "Case #{}: {}".format(i, fcn(As, K))
  # check out .format's specification for more formatting options
