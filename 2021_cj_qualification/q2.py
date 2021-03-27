import sys

sys.setrecursionlimit(10000)

def fcn(x,y,string):
    c = 0
    ht = dict()
    def rec(cur_str, index):
        nonlocal c
        c += 1
        ht_key = None
        if index > 0:
            ht_key = ''.join(cur_str[index-1:])
            if ht_key in ht:
                return ht[ht_key]
        # print(cur_str, index, x, y)
        if index == len(cur_str):
            return 0
        res = 0
        if cur_str[index] == '?':
            cur_str[index] = 'C'
            optionA = rec(cur_str, index+1)
            if index > 0 and ''.join(cur_str[index-1:index+1]) == 'JC':
                optionA += y
            cur_str[index] = 'J'
            res = rec(cur_str, index+1)
            if index > 0 and ''.join(cur_str[index-1:index+1]) == 'CJ':
                res += x
            cur_str[index] = '?'
            res = min(res, optionA)
        elif cur_str[index] == 'C':
            res = rec(cur_str, index+1)
            if index > 0 and ''.join(cur_str[index-1:index+1]) == 'JC':
                res += y
        elif cur_str[index] == 'J':
            res = rec(cur_str, index+1)
            if index > 0 and ''.join(cur_str[index-1:index+1]) == 'CJ':
                res += x
        else:
            assert False
        if index > 0:
            ht[ht_key] = res
        return res
    result = rec(string, 0)
    # print(c)
    return result


t = int(input())  # read a line with a single integer
for i in range(1, t + 1):
    x,y,string = [s for s in input().split(" ")]  # read a list of integers, 2 in this case
    print("Case #{}: {}".format(i, fcn(int(x), int(y), list(string))))
