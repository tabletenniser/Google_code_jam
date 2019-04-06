def fcn(array, n):
    total = 0
    ppl_remain = n
    round_down_list = []
    for num in array:
        percentage = num * 100.0 / n
        total += int(round(percentage))
        percentage_diff = percentage - int(percentage)
        if 0 < percentage_diff < 0.5:
            round_down_list.append(percentage_diff)
        ppl_remain -= num

    round_down_list.sort()
    # print "ppl_reamin:", ppl_remain
    # print "round_down_list:", round_down_list
    while ppl_remain > 0:
        percentage = 100.0 / n
        total += int(round(percentage))
        percentage_diff = percentage - int(percentage)
        if len(round_down_list) == 0:
            if 0 < percentage_diff < 0.5:
                round_down_list.append(percentage_diff)
                round_down_list.sort()
        elif 0 < percentage_diff < 0.5:
            round_down_list[-1] += percentage_diff
            if round_down_list[-1] >=0.5:
                total += 1
                del round_down_list[-1]
        ppl_remain -= 1
    return total

def fcn2(array, n):
    total = 0
    ppl_remain = n
    percentage_lst = []
    for num in array:
        percentage = num * 100.0 / n
        percentage_lst.append(percentage)
        total += int(round(percentage))
        ppl_remain -= num

    print "ppl_reamin:", ppl_remain
    print "total:", total
    print "percentage_lst:", percentage_lst
    while ppl_remain > 0:
        ppl_remain -= 1
        percentage = 100.0/n
        if percentage - int(percentage) >= 0.5 or percentage - int(percentage) == 0:
            total += int(round(percentage))
            percentage_lst.append(percentage)
            print "total to new:", total
            continue
        has_added = False
        max_pct_index = 0
        max_pct = 0
        for i in xrange(len(percentage_lst)):
            p = percentage_lst[i]
            if p - int(p) < 0.5 and p - int(p) > max_pct:
                max_pct = p - int(p)
                max_pct_index = i
            new_p = p + percentage
            if p - int(p) < 0.5 and new_p - int(new_p) >= 0.5:
                total += int(round(new_p)) - int(round(p))
                print "total to existing:", total
                percentage_lst[i] = new_p
                has_added = True
                break
        if not has_added:
            percentage_lst[max_pct_index]
        print "ppl_reamin:", ppl_remain
    return total

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    n, l = [int(s) for s in raw_input().split(" ")]  # read a list of integers, 2 in this case
    array = [int(s) for s in raw_input().split(" ")]  # read a list of integers, 2 in this case
    assert len(array) == l
    print "Case #{}: {}".format(i, fcn(array, n))
