def fcn_1(array, n):
    if array[0] == 0 or array[-1] == 0:
        return "IMPOSSIBLE"
    roll_left_quota = 0
    roll_right_req = 0
    max_balls_ever = 0
    for num in array:
        if num == 0:
            roll_left_quota += 1
        elif num - 1 >= roll_left_quota:    # more balls than quota, need to roll right
            leftover_to_roll_right = (num - 1) - roll_left_quota
            max_balls_ever = max(roll_left_quota, leftover_to_roll_right)
            roll_right_req += leftover_to_roll_right
            roll_left_quota = 0
        else:   # roll all balls to the left should be enough
            roll_right_req = 0
            roll_left_quota -= (num - 1)
            max_balls_ever = roll_left_quota

        max_balls_ever = max(max_balls_ever, cur_balls_available)

    if cur_balls_available == 0:
        return max_balls_ever
    return "IMPOSSIBLE"

def fcn(array, n):
    if array[0] == 0 or array[-1] == 0:
        return "IMPOSSIBLE"
    target = [1 for _ in xrange(n)]
    layer = 0
    solution = []
    def fcn_rec(arr):
        layer = []
        roll_left_quota = 0
        roll_right_req = 0
        next_arr = [0 for _ in xrange(n)]
        for i in xrange(n):
            num = arr[i]
            if roll_right_req > 0:
                layer.append('/')
                next_arr[i] = arr[i] - (roll_right_req - 1)
                next_arr[i+1] += arr[i] + (roll_right_req - 1)
                next_arr[i] = arr[i]
            if num == 0:
                roll_left_quota += 1
            else:
                roll_right_req += (num - 1) - roll_left_quota

    return fcn_rec(arr)

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    c = int(raw_input())  # read a list of integers, 2 in this case
    array = [int(s) for s in raw_input().split(" ")]  # read a list of integers, 2 in this case
    assert len(array) == c
    print "Case #{}: {}".format(i, fcn(array, c))
