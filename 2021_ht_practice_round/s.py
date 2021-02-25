import random
import sys
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, teams, pizzas):
        self.ct_two, self.ct_three, self.ct_four = teams
        self.pizzas = pizzas
        self.pizzas.sort(key=lambda s: len(s[1])+random.random(), reverse=True)

    def get_opt_solution(self):
        sol = []
        score = 0
        while True:
            ing = set()
            if len(self.pizzas) > 5 and self.ct_four > 0:
                sol.append(self.pizzas[:4])
                for p in self.pizzas[:4]:
                    ing = ing.union(p[1])
                score += len(ing) ** 2
                self.ct_four -= 1
                self.pizzas = self.pizzas[4:]
            elif len(self.pizzas) >= 3 and self.ct_three > 0:
                sol.append(self.pizzas[:3])
                for p in self.pizzas[:3]:
                    ing = ing.union(p[1])
                score += len(ing) ** 2
                self.ct_three -= 1
                self.pizzas = self.pizzas[3:]
            elif len(self.pizzas) >= 2 and self.ct_two > 0:
                sol.append(self.pizzas[:2])
                for p in self.pizzas[:2]:
                    ing = ing.union(p[1])
                score += len(ing) ** 2
                self.ct_two -= 1
                self.pizzas = self.pizzas[2:]
            else:
                break
        return sol, score

teams = [int(s) for s in input().strip().split(" ")]
pizza_cnt = teams[0]
pizzas = []
for index in range(pizza_cnt):
    pizzas.append((index, set([s for s in input().split(" ")][1:])))

opt_sol = None
max_score = -1
i = 0 
start = time.time()
while time.time() - start < 300 and i < 500: # 2 minutes
    s = Solution(teams[1:], pizzas)
    sol, score=s.get_opt_solution()
    if score > max_score:
        eprint(i, score, time.time()-start)
        max_score = score
        opt_sol = sol
    i += 1

print(len(opt_sol))
for line in opt_sol:
    orders = ' '.join([str(p[0]) for p in line])
    print(len(line), orders)
