import math

def nCr(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def fcn(W, H, L, U, R, D):
    res = 0.0
    r, u = R + 1, U - 1
    while r <= W and u >= 1:
        # print('1:',r,u,W)
        if r == W and u > 1:
            res += 1 / 2 ** (r - 1)
            res += nCr(r + u -3, r-2) / 2 ** (r + u - 2)
            break
        res += nCr(r + u -2, r-1) / 2 ** (r + u - 2)
        r += 1
        u -= 1
    d, l = D + 1, L - 1
    while d <= H and l >= 1:
        # print('2:',d,l,H)
        if d == H and l > 1:
            res += 1 / 2 ** (d - 1)
            res += nCr(d + l -3, d-2) / 2 ** (d + l - 2)
            break
        res += nCr(d + l -2, d-1) / 2 ** (d + l - 2)
        d += 1
        l -= 1
    return res

t = int(input())
for i in range(1, t + 1):
    W, H, L, U, R, D = [int(s) for s in input().split(" ")]
    res = fcn(W, H, L, U, R, D)
    print("Case #{}: {}".format(i, res))
