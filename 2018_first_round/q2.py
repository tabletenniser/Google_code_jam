def check_array(array):
    if len(array) <= 2:
        return len(array), 1

    first_cand = set()
    second_cand = set()
    candidates = []
    for i in xrange(len(array)):
        e1, w1 = array[i]
        if e1 not in first_cand and w1 not in second_cand:
            prev_elem = first_cand.pop()
            candidates.append(prev_elem[0], w1)
            candidates.append(e1, prev_elem[1])
        elif len(candidates) == 2:
            if candidates[0][0] == e1 and candidates[1][1] != w1  or candidates[0][1] == w1 and candidates[1][0] != e1:
                del candidates[1]
            elif candidates[0][0] != e1 and candidates[1][1] == w1  or candidates[0][1] != w1 and candidates[1][0] == e1:
                del candidates[0]
            elif candidates[0][0] == e1 and candidates[1][1] == w1 or candidates[0][1] == w1 and candidates[1][0] == e1:
                pass
            else:
                max_len = cur_len
        else:
            first_cand.add(e1)
            second_cand.add(w1)


    return None, None

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    _size = int(raw_input())
    array = []
    for i in xrange(1, _size + 1):
        d, a, b = [int(s) for s in raw_input().split(" ")] 
        array.append((d+a, d-b))
    answer = check_array(array)
    print "Case #{}: {} {}".format(i, answer[0], answer[1])
