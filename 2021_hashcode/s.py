import random
import sys
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, intersections, vehicles):
        self.streets = streets
        self.vehicles = vehicles
        self.intersections = intersections
        eprint(streets)
        eprint(intersections)
        eprint(vehicles)

    def get_opt_solution(self):
        sol = []
        for ind in intersections:
            incoming_streets = intersections[ind]
            sol.append((ind, [next(iter(incoming_streets)), 2]))
        return sol

D, I, S, V, F = [int(s) for s in input().strip().split(" ")]
streets = {}
intersections = {}
for index in range(S):
    B, E, name, length = [s for s in input().split(" ")]
    inter = intersections.get(B, set())
    inter.add(name)
    intersections[B] = inter
    inter = intersections.get(E, set())
    inter.add(name)
    intersections[E] = inter
    streets[name] = ({B, E}, length)

vehicles = []
for index in range(V):
    vehicles.append([s for s in input().split(" ")][1:])


s = Solution(streets, intersections, vehicles)
opt_sol=s.get_opt_solution()

# opt_sol = None
# max_score = -1
# i = 0 
# start = time.time()
# while time.time() - start < 300 and i < 500: # 2 minutes
#     s = Solution(teams[1:], pizzas)
#     sol, score=s.get_opt_solution()
#     if score > max_score:
#         eprint(i, score, time.time()-start)
#         max_score = score
#         opt_sol = sol
#     i += 1

eprint("Solution:", opt_sol)
print(len(opt_sol))
for line in opt_sol:
    print(line[0])
    signals = line[1]
    print(signals)
    for sig in signals:
        print(signals)
    orders = ' '.join([str(p[0]) for p in line])
    print(len(line), orders)
