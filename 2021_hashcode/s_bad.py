import random
import sys
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, incoming, outgoing, vehicles, D):
        self.streets = streets
        self.vehicles = vehicles
        self.incoming = incoming
        self.outgoing = outgoing
        self.D = D
        self.street_lengths = [s[1] for s in streets]
        self.street_frequency = {}
        for v in vehicles:
            for s in v:
                self.street_frequency[s] = self.street_frequency.get(s, 0)+1
        # eprint(streets)
        # eprint(vehicles)
        # eprint(self.street_frequency)

    def get_opt_solution(self):
        sol = {}
        for ind in self.incoming:
            incoming_streets = self.incoming[ind]
            schedule = []
            total_sum = 1
            for st in incoming_streets:
                value = self.street_frequency.get(st, 0)
                total_sum += value
            for st in incoming_streets:
                value = min(int(self.street_frequency.get(st, 0) / total_sum * 100), self.D)
                if value > 0:
                    schedule.append((st, value))
            if len(schedule) == 0:
                schedule.append((next(iter(incoming_streets)), 2))
            sol[ind] = schedule
        self.sol = sol
        return sol

    def _nextGreen(self, cur, intersection_index, street):
        schedule = self.sol[intersection_index]
        return 2

    def evaluate(self, D, F):
        score = 0
        for streets_to_travel in self.vehicles:
            cur_time = 0
            for street in streets_to_travel:
                (b, e), t = self.streets[street]
                cur_time = self._nextGreen(cur_time+int(t), e, street)
                if cur_time > D:
                    break
            if cur_time <= D:
                score += (D - cur_time) + F
        return score

D, I, S, V, F = [int(s) for s in input().strip().split(" ")]
streets = {}
incoming = {}
outgoing = {}
for index in range(S):
    B, E, name, length = [s for s in input().split(" ")]
    inter = outgoing.get(B, set())
    inter.add(name)
    outgoing[B] = inter
    inter = incoming.get(E, set())
    inter.add(name)
    incoming[E] = inter
    streets[name] = ((B, E), length)

vehicles = []
for index in range(V):
    vehicles.append([s for s in input().split(" ")][1:])


s = Solution(streets, incoming, outgoing, vehicles, D)
opt_sol=s.get_opt_solution()
# eprint(s.evaluate(D, F))

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
for key in opt_sol:
    print(key) # intersection index
    signals = opt_sol[key]
    print(len(signals))
    for sig in signals:
        print(' '.join([str(p) for p in sig]))
