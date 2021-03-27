import sys

T, N, Q= [int(s)for s in input().split(" ")]
for i in range(1, T + 1):
    j = 0
    cur_arr = [1, 2]
    cur_num = 3
    while len(cur_arr) < N:
        l, r = 0, len(cur_arr)
        while l < r:
            if r == l + 1:
                if l > 0:
                    l -= 1
                else:
                    r += 1
            mid1 = l + (r - l) //3
            mid2 = r - (r - l+1) //3
            # print('index:', l, mid1, mid2, r, file=sys.stderr)
            print(cur_arr[mid1], cur_arr[mid2], cur_num)
            median = int(input())
            j += 1
            # print('Input:', cur_arr[mid1], cur_arr[mid2], cur_num, file=sys.stderr)
            # print('Output:', median, file=sys.stderr)
            if median == cur_num:
                l = mid1+1
                r = mid2
            elif median == cur_arr[mid1]:
                r = mid1
            elif median == cur_arr[mid2]:
                l = mid2+1
            # else:
            #     assert False
        cur_arr.insert(l, cur_num)
        # print('Current array: ', cur_arr, file=sys.stderr)
        cur_num += 1
    print(' '.join([str(elem) for elem in cur_arr]))
    # print('Guessed answer:', ' '.join([str(elem) for elem in cur_arr]), file=sys.stderr)
    res = int(input())
