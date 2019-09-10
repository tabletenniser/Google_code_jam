cache = {}
def find_interactions(x, y, people):
    if (x,y,people) in cache:
        return cache[(x,y,people)]
    result = 0
    for p in people:
        if p[2] == 'N' and y > p[1]:
            result += 1
        if p[2] == 'S' and y < p[1]:
            result += 1
        if p[2] == 'E' and x > p[0]:
            result += 1
        if p[2] == 'W' and x < p[0]:
            result += 1
    cache[x, y, people] = result
    return result

def fcn(people, q):
    cur_max = find_interactions(0, 0, people)
    result = 0, 0
    x_s, y_s = [0], [0]
    for p in people:
        if p[2] == 'N' and p[1] < q:
            y_s.append(p[1] + 1)
        if p[2] == 'S' and p[1] > 0:
            y_s.append(p[1] - 1)
        if p[2] == 'E' and p[0] < q:
            x_s.append(p[0] + 1)
        if p[2] == 'W' and p[0] > 0:
            x_s.append(p[0] - 1)

    for x in x_s:
        for y in y_s:
            ans = find_interactions(x, y, people)
            # print 'Cur:', x, y, ans
            if ans > cur_max or (ans == cur_max and \
                    (x < result[0] or x == result[0] and y < result[1])):
                result = x, y
                cur_max = ans
    return result

t = int(raw_input())
for i in xrange(1, t + 1):
    p, q = [int(s) for s in raw_input().split(" ")]
    people = []
    for j in xrange(1, p + 1):
        x, y, d = [s for s in raw_input().split(" ")]
        people.append((int(x), int(y), d))
    result = fcn(tuple(people), q + 1)
    print "Case #{}: {} {}".format(i, result[0], result[1])
    # check out .format's specification for more formatting options
