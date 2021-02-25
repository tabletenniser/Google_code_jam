import random
import sys
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, incoming, outgoing, vehicles):
        self.streets = streets
        self.vehicles = vehicles
        self.incoming = outgoing
        self.outgoing = outgoing
        # eprint(streets)
        # eprint(intersections)
        # eprint(vehicles)

    def get_opt_solution(self):
        sol = []
        for ind in self.incoming:
            incoming_streets = self.incoming[ind]
            sol.append((ind, [(next(iter(incoming_streets)), 2)]))
        return sol

D, I, S, V, F = [int(s) for s in input().strip().split(" ")]
streets = {}
incoming = {}
outgoing = {}
for index in range(S):
    B, E, name, length = [s for s in input().split(" ")]
    inter = incoming.get(B, set())
    inter.add(name)
    incoming[B] = inter
    inter = outgoing.get(E, set())
    inter.add(name)
    outgoing[E] = inter
    streets[name] = ((B, E), length)

vehicles = []
for index in range(V):
    vehicles.append([s for s in input().split(" ")][1:])


s = Solution(streets, incoming, outgoing, vehicles)
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

# eprint("Solution:", opt_sol)
print(len(opt_sol))
for line in opt_sol:
    print(line[0]) # intersection index
    signals = line[1]
    print(len(signals))
    for sig in signals:
        print(' '.join([str(p) for p in sig]))
