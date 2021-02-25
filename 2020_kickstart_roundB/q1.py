def fcn(arr):
    res = 0
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i+1]:
            res += 1
    return res

t = int(input())
for i in range(1, t + 1):
    _ = int(input())
    arr = [int(s) for s in input().split(" ")]
    result = fcn(arr)
    print("Case #{}: {}".format(i, result))
