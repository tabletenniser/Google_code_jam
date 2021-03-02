import random
import sys
import time
import heapq
from collections import namedtuple,defaultdict

queuedCar = namedtuple('queuedCar', ['time_to_leave','cur_street','remaining_path'])
Street = namedtuple('Street', ['name', 'begin', 'end', 'length'])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, incoming, outgoing, vehicles, D):
        self.streets = streets
        self.vehicles = vehicles
        self.incoming = incoming # dict mapping interection ==> set(streets)
        self.outgoing = outgoing
        self.D = D
        self.street_lengths = {s: int(streets[s].length) for s in streets}
        self.street_frequency = {}
        for v in vehicles:
            for s in v:
                self.street_frequency[s] = self.street_frequency.get(s, 0)+1
        # eprint("streets:", streets)
        # eprint("vehicles:", vehicles)
        # eprint("street_frequency:", self.street_frequency)
        # eprint("street_lengths:", self.street_lengths)
        # eprint("incoming:", self.incoming)

    def get_opt_solution(self):
        sol = {}
        for ind in self.incoming:
            incoming_streets = self.incoming[ind]
            schedule = []
            total_sum = 1
            for st in incoming_streets:
                value = self.street_frequency.get(st, 0)
                total_sum += value
            # iterating over a set doesn't gurantee the order
            for st in sorted(incoming_streets):
                value = min(int(self.street_frequency.get(st, 1) / total_sum * 9), self.D)
                value = max(value, 1)
                schedule.append((st, value))
            sol[ind] = schedule
        self.sol = sol
        return sol

    # def _canPass(self, cur_time, street):
    #     inter = self.streets[street].E
    #     schedule = self.sol[inter]
    #     cycle_time = sum([s[1] for s in schedule])
    #     mod = cur_time % cycle_time
    #     for s in schedule:
    #         mod -= s[1]
    #         if mod <= 0:
    #             cur_st = s[0]
    #             break
    #     return street == cur_st

    def _getNextAllowedTime(self, incoming_street, earliest_time):
        inter = self.streets[incoming_street].end
        schedule = self.sol[inter]
        cycle_time = sum([s[1] for s in schedule])
        cur_sim_time = earliest_time - earliest_time % cycle_time
        street_index = 0
        while cur_sim_time < earliest_time:
            cur_sim_time += schedule[street_index][1]
            if cur_sim_time > earliest_time and schedule[street_index][0] == incoming_street:
                return earliest_time

            street_index = (street_index + 1) % len(schedule)
        while schedule[street_index][0] != incoming_street:
            cur_sim_time += schedule[street_index][1]
            street_index = (street_index + 1) % len(schedule)
        return cur_sim_time

    def evaluate(self, D, F):
        # global priority queue storing first car of each intersection ordered by first allowed time to pass
        first_cars_pq = []
        street_to_queues = defaultdict(list)
        for car in self.vehicles:
            cur_street_name = car[0]
            remaining_path = car[1:]
            inter = self.streets[cur_street_name].end
            time_to_leave = self._getNextAllowedTime(cur_street_name, 0)
            queued_car = queuedCar(time_to_leave, cur_street_name, remaining_path)
            if cur_street_name not in street_to_queues or len(street_to_queues[cur_street_name])== 0:
                heapq.heappush(first_cars_pq, queued_car)
            street_to_queues[cur_street_name].append(queued_car)

        score = 0
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_street_name = cur_car.cur_street
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car.remaining_path[0]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if len(cur_car.remaining_path) == 1 and arrival_at_next_inter <= D:
                score += F + (D - arrival_at_next_inter)
            else:
                time_to_leave_next_inter = self._getNextAllowedTime(outgoing_street_name, arrival_at_next_inter)
                queued_car = queuedCar(time_to_leave_next_inter, outgoing_street_name, cur_car.remaining_path[1:])
                if outgoing_street_name not in street_to_queues or len(street_to_queues[outgoing_street_name])== 0:
                    heapq.heappush(first_cars_pq, queued_car)
                street_to_queues[outgoing_street_name].append(queued_car)
            if len(street_to_queues[cur_street_name]) > 0:
                next_car_in_queue = street_to_queues[cur_street_name][0]
                time_to_leave = self._getNextAllowedTime(cur_street_name, max(cur_car.time_to_leave+1, next_car_in_queue.time_to_leave))
                heapq.heappush(first_cars_pq, queuedCar(time_to_leave, next_car_in_queue.cur_street, next_car_in_queue.remaining_path))
        return score


    def evaluate2(self, D, F):
        score = 0
        cnt = 0
        vehicle_location = []
        congestion = {}
        for v in self.vehicles:
            vehicle_location.append([0, self.street_lengths[v[0]]])
        for cur_time in range(0, D+1):
            if cnt == len(self.vehicles):
                break
            # eprint(cur_time, vehicle_location, self.vehicles)
            for i, (v, s_l) in enumerate(zip(self.vehicles, vehicle_location)):
                if s_l[0] == len(v):
                    continue
                if s_l[1] > 0:
                    vehicle_location[i][1] -= 1
                st = v[vehicle_location[i][0]]
                if vehicle_location[i][1] == 0:
                    if not self._canPass(cur_time, st):
                        cong_list = congestion.get(st, list())
                        cong_list.append(i)
                        congestion[st] = cong_list
                    elif st not in congestion or len(congestion[st]) == 0 or congestion[st][0] == i:
                        if st in congestion and len(congestion[st]) > 0 and  congestion[st][0] == i:
                            congestion[st] = congestion[st][1:]
                        vehicle_location[i][0] += 1
                        if vehicle_location[i][0] == len(v):
                            score += (D - cur_time) + F
                            cnt += 1
                        else:
                            new_st = v[vehicle_location[i][0]]
                            vehicle_location[i][1] = self.street_lengths[new_st]
        return score, cnt

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
    streets[name] = Street(name, B, E, int(length))

vehicles = []
for index in range(V):
    vehicles.append([s for s in input().split(" ")][1:])


s = Solution(streets, incoming, outgoing, vehicles, D)
opt_sol=s.get_opt_solution()
eprint('Score:', s.evaluate(D, F))

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
