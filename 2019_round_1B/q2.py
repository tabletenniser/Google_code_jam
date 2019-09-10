def check_array(array):
    swap_happened = True
    while swap_happened:
        unsorted_index = -1
        swap_happened = False
        for i in xrange(len(array) - 2):
            if unsorted_index == -1 and array[i+1] < array[i]:
                unsorted_index = i
            if array[i] > array[i+2]:
                array[i], array[i+2] = array[i+2], array[i]
                swap_happened = True
        #     print array
        # print '===='
    if unsorted_index == -1:
        if array[-1] < array[-2]:
            return len(array) - 2
        return "ok"
    return unsorted_index

# raw_input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Kickstart problems.
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
  _size = int(raw_input())
  array = [int(s) for s in raw_input().split(" ")]  # read a list of integers, 2 in this case
  assert(len(array) == _size)
  print "Case #{}: {}".format(i, check_array(array))
  # check out .format's specification for more formatting options
