import random
import sys
import math
import time
import heapq
from collections import namedtuple,defaultdict
import random

MAX_INT = 10000000

queuedCar = namedtuple('queuedCar', ['time_to_leave','cur_street','remaining_path'])
Street = namedtuple('Street', ['name', 'begin', 'end', 'length'])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, incoming, outgoing, vehicles, D, car_limit):
        self.streets = streets
        self.incoming = incoming # dict mapping interection ==> set(streets)
        self.outgoing = outgoing
        self.D = D
        self.street_frequency = {}
        vehicle_path_length_pair = []
        self.max_street_length = max([s.length for s in self.streets.values()])
        for v in vehicles:
            length = 0
            for s in v[:-1]:
                self.street_frequency[s] = self.street_frequency.get(s, 0)+1
                length = self.streets[s].length
            vehicle_path_length_pair.append((length, v))
        vehicle_path_length_pair.sort()
        self.vehicles = vehicle_path_length_pair[:car_limit]
        # eprint("streets:", streets)
        # eprint("vehicles:", vehicles)
        # eprint("street_frequency:", self.street_frequency)
        # eprint("incoming:", self.incoming)

    def get_sim_solution(self, street_names, max_green_light_length, s_length_factor):
        street_freq = dict()
        street_arrival_time = defaultdict(list)
        for name_arrival_time_pair in street_names:
            sn = name_arrival_time_pair[0]
            street_freq[sn] = street_freq.get(sn, 0)+1
            street_arrival_time[sn].append(name_arrival_time_pair[1])
        sol = {}
        for incoming_i in self.incoming:
            incoming_streets = self.incoming[incoming_i]
            total_sum = 1
            for st in incoming_streets:
                total_sum += street_freq.get(st, 0)
            # iterating over a set doesn't gurantee the order
            # sort first to avoid undeterminicity
            incoming_streets = list(filter(lambda x: x in street_freq and street_freq[x] > 0, incoming_streets))
            # TODO: Find a way to calculate actual cycle_time
            num_incoming_sts = len(incoming_streets)
            streets = sorted(list(incoming_streets))
            streets.sort(key=lambda x:sum([y % num_incoming_sts for y in street_arrival_time[x]])/(len(street_arrival_time[x])+1))
            # random.shuffle(streets)
            # max_green_light_length = random.randint(1, 30)
            schedule = [None for _ in range(num_incoming_sts)]
            # schedule = []
            for st in incoming_streets:
                s_length_v = int(self.streets[st].length / self.max_street_length * s_length_factor)
                value = s_length_v + math.ceil(street_freq.get(st, 0) / total_sum * max_green_light_length)
                ind = 0
                if st in street_arrival_time:
                    ind = min(street_arrival_time[st]) % num_incoming_sts
                while schedule[ind] is not None:
                    ind = (ind+ 1) % num_incoming_sts
                schedule[ind] = (st, 1)
                # schedule.append((st, min(value, self.D)))
            if len(schedule) == 0:
                schedule.append((streets[0], 1))
            sol[incoming_i] = schedule
        self.sol = sol
        return sol

    def get_opt_solution(self, max_green_light_length):
        sol = {}
        for ind in self.incoming:
            incoming_streets = self.incoming[ind]
            schedule = []
            total_sum = 1
            for st in incoming_streets:
                total_sum += self.street_frequency.get(st, 0)
            # iterating over a set doesn't gurantee the order
            streets = list(incoming_streets)
            # random.shuffle(streets)
            streets.sort()
            for st in streets[::-1]:
                value = min(int(self.street_frequency.get(st, 0) / total_sum * max_green_light_length), self.D)
                if value > 0:
                    schedule.append((st, value))
                elif len(schedule) == 0:
                    schedule.append((st, 1))
            sol[ind] = schedule
        self.sol = sol
        return sol

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
        i = 0
        while schedule[street_index][0] != incoming_street:
            cur_sim_time += schedule[street_index][1]
            street_index = (street_index + 1) % len(schedule)
            i += 1
            if i > len(schedule):
                return MAX_INT
        cur_wait_time = cur_sim_time - earliest_time
        # if cur_wait_time > 260:
        #     eprint('Long wait:', incoming_street, earliest_time, cur_sim_time)
        self.max_wait_time = max(self.max_wait_time, cur_wait_time)
        return cur_sim_time

    def evaluate(self, D, F):
        self.max_wait_time = 0
        # global priority queue storing first car of each intersection ordered by first allowed time to pass
        first_cars_pq = []
        street_to_queues = defaultdict(list)
        for length_car_pair in self.vehicles:
            car = length_car_pair[1]
            cur_street_name = car[0]
            remaining_path = car[1:]
            inter = self.streets[cur_street_name].end
            time_to_leave = self._getNextAllowedTime(cur_street_name, 0)
            queued_car = queuedCar(time_to_leave, cur_street_name, remaining_path)
            if cur_street_name not in street_to_queues or len(street_to_queues[cur_street_name])== 0:
                heapq.heappush(first_cars_pq, queued_car)
            street_to_queues[cur_street_name].append(queued_car)

        score = 0
        cars_passed = 0
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_street_name = cur_car.cur_street
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car.remaining_path[0]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if len(cur_car.remaining_path) == 1 and arrival_at_next_inter <= D:
                score += F + (D - arrival_at_next_inter)
                cars_passed += 1
            # elif len(cur_car.remaining_path) > 1:
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
        return score, cars_passed

    def simulate(self, D, F):
        # global priority queue storing first car of each intersection ordered by first allowed time to pass
        first_cars_pq = []
        street_to_queues = defaultdict(list)
        street_names_to_return = []
        for length_car_pair in self.vehicles:
            car = length_car_pair[1]
            cur_street_name = car[0]
            remaining_path = car[1:]
            inter = self.streets[cur_street_name].end
            time_to_leave = 0
            queued_car = queuedCar(time_to_leave, cur_street_name, remaining_path)
            if cur_street_name not in street_to_queues or len(street_to_queues[cur_street_name])== 0:
                heapq.heappush(first_cars_pq, queued_car)
            street_to_queues[cur_street_name].append(queued_car)

        score = 0
        cars_passed = 0
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_street_name = cur_car.cur_street
            street_names_to_return.append((cur_street_name, cur_car.time_to_leave))
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car.remaining_path[0]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if len(cur_car.remaining_path) == 1 and arrival_at_next_inter <= D:
                score += F + (D - arrival_at_next_inter)
                cars_passed += 1
            elif len(cur_car.remaining_path) > 1:
                time_to_leave_next_inter = arrival_at_next_inter
                queued_car = queuedCar(time_to_leave_next_inter, outgoing_street_name, cur_car.remaining_path[1:])
                if outgoing_street_name not in street_to_queues or len(street_to_queues[outgoing_street_name])== 0:
                    heapq.heappush(first_cars_pq, queued_car)
                street_to_queues[outgoing_street_name].append(queued_car)
            if len(street_to_queues[cur_street_name]) > 0:
                next_car_in_queue = street_to_queues[cur_street_name][0]
                time_to_leave = max(cur_car.time_to_leave+1, next_car_in_queue.time_to_leave)
                heapq.heappush(first_cars_pq, queuedCar(time_to_leave, next_car_in_queue.cur_street, next_car_in_queue.remaining_path))
        return street_names_to_return, score, cars_passed

    def _canPass(self, cur_time, street):
        inter = self.streets[street].E
        schedule = self.sol[inter]
        cycle_time = sum([s[1] for s in schedule])
        mod = cur_time % cycle_time
        for s in schedule:
            mod -= s[1]
            if mod <= 0:
                cur_st = s[0]
                break
        return street == cur_st
    def evaluate_bad(self, D, F):
        score = 0
        cnt = 0
        vehicle_location = []
        congestion = {}
        for pair in self.vehicles:
            v = pair[1]
            vehicle_location.append([0, self.streets[v[0]].length])
        for cur_time in range(0, D+1):
            if cnt == len(self.vehicles):
                break
            for i, (pair, s_l) in enumerate(zip(self.vehicles, vehicle_location)):
                v = pair[1]
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
                            vehicle_location[i][1] = self.streets[new_st].length
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


opt_sol = None
max_score = -1
i = 0 
s = Solution(streets, incoming, outgoing, vehicles, D, len(vehicles))
# eprint('Abs max score', abs_max_score, cars_passed, len(vehicles), sim_street_names)
start = time.time()
MAX_ITER = 1
while time.time() - start < 1200 and i < MAX_ITER:
    # dropping_vehicles = random.randint(0, 30)
    dropping_vehicles = i
    s = Solution(streets, incoming, outgoing, vehicles, D, len(vehicles)-dropping_vehicles)
    sim_street_names, abs_max_score, cars_passed = s.simulate(D, F)
    # eprint(i, 'Simuate score', abs_max_score, len(sim_street_names), cars_passed, len(vehicles))
    # max_green_light_length = random.randint(1, 15)
    max_green_light_length = 1
    # sol=s.get_opt_solution(max_green_light_length)
    sol=s.get_sim_solution(sim_street_names, max_green_light_length, 0)
    score,cars_passed = s.evaluate(D, F)
    # eprint(i, 'Cur score:', score, 'max wait time:', s.max_wait_time, 'cars passed', cars_passed, time.time()-start, 'max_green_light_length', max_green_light_length)
    if score > max_score:
        eprint('Max score at: ', i, score, 'max wait time:', s.max_wait_time, 'cars passed', cars_passed, time.time()-start, 'max_green_light_length', max_green_light_length, dropping_vehicles)
        max_score = score
        opt_sol = sol
    i += 1

# s = Solution(streets, incoming, outgoing, vehicles, D)
# opt_sol=s.get_opt_solution(9)
# eprint('Score:', s.evaluate(D, F))
print(len(opt_sol))
for key in opt_sol:
    print(key) # intersection index
    signals = opt_sol[key]
    print(len(signals))
    for sig in signals:
        print(' '.join([str(p) for p in sig]))
