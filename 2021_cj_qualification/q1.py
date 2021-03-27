def fcn(array):
    L = len(array)
    res = 0
    for i in range(L-1):
        cur_min = array[i]
        cur_min_index = i
        for j in range(i+1, L):
            if array[j] < cur_min:
                cur_min = array[j]
                cur_min_index = j
        res += cur_min_index - i + 1
        array[i:cur_min_index+1] = array[i:cur_min_index+1][::-1]
        # print(array)
    return res


# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(input())  # read a line with a single integer
for i in range(1, t + 1):
    _ = int(input())  # read a list of integers, 2 in this case
    array = [int(s) for s in input().split(" ")]  # read a list of integers, 2 in this case
    print("Case #{}: {}".format(i, fcn(array)))
