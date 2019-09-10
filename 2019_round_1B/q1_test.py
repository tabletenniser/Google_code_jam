from q1 import fcn, find_interactions
import random

N = 10
matrix = [[0 for _ in xrange(N)] for _ in xrange(N)]

for _ in xrange(10000):
    people = []
    for i in xrange(random.randint(1, 20)):
        x,y,d = random.randint(0, N-1), random.randint(0, N-1), random.choice(['N', 'S', 'W', 'E'])
        people.append((x,y,d))

    result = fcn(tuple(people), N)
    cur_max = 0
    correct_result = 0,0
    for i in xrange(N + 1):
        for j in xrange(N + 1):
            r = find_interactions(i, j, tuple(people))
            if r > cur_max:
                cur_max = r
                correct_result = (i, j)
    print tuple(people), N
    print result, correct_result, cur_max, len(people)
    assert correct_result == result
