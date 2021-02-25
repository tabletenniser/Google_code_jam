def fcn(buses, max_date):
    dates = set()
    m_date = max_date
    for b in buses[::-1]:
        # print(b, dates)
        for d in dates:
            if d % b == 0:
                continue
        multiplier = m_date // b
        d = multiplier * b
        m_date = d
        dates.add(d)
    return min(dates)

t = int(input())
for i in range(1, t + 1):
    _, max_date = [int(s) for s in input().split(" ")]
    buses = [int(s) for s in input().split(" ")]
    result = fcn(buses, max_date)
    print("Case #{}: {}".format(i, result))
