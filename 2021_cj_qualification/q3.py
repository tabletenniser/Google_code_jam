def evaluate(array):
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

def fcn(N, C):
    if C < N - 1:
        return 'IMPOSSIBLE'
    ops = C - (N-1)
    arr = [i+1 for i in range(N)]
    for i in range(N-2, -1, -1):
        j = min(i + ops, N - 1)
        arr[i:j+1] = arr[i:j+1][::-1]
        ops -= (j - i)
        if ops <= 0:
            # print(C, evaluate(arr))
            return ' '.join([str(elem) for elem in arr])
    return 'IMPOSSIBLE'

t = int(input())  # read a line with a single integer
for i in range(1, t + 1):
    N, C = [int(s)for s in input().split(" ")]
    print("Case #{}: {}".format(i, fcn(N, C)))
