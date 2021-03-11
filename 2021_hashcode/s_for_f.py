import sys
import math
import time
import heapq
from collections import namedtuple,defaultdict
import random
import copy

MAX_INT = 10000000

queuedCar = namedtuple('queuedCar', ['time_to_leave','car_i','path_j'])
Street = namedtuple('Street', ['name', 'begin', 'end', 'length'])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, incoming, outgoing, vehicles, D):
        self.streets = streets
        self.incoming = incoming # dict mapping interection ==> set(streets)
        self.outgoing = outgoing
        self.D = D
        self.street_frequency = {}
        self.max_street_length = max([s.length for s in self.streets.values()])
        self.vehicles = vehicles
        for _,v in vehicles.items():
            for s in v[:-1]:
                self.street_frequency[s] = self.street_frequency.get(s, 0)+1
        # eprint("streets:", streets)
        # eprint("vehicles:", vehicles)
        # eprint("street_frequency:", self.street_frequency)
        # eprint("incoming:", self.incoming)

    def get_sim_solution(self, street_names, max_max_green_light_length, max_total_sum, road_percent):
        street_freq = dict()
        street_first_car = dict()
        for name_arrival_time_pair in street_names:
            sn = name_arrival_time_pair[0]
            street_freq[sn] = street_freq.get(sn, 0)+1
            street_first_car[sn] = min(street_first_car.get(sn, MAX_INT), name_arrival_time_pair[1])
        sol = {}
        new_max_inter_sum = 1
        for ind in self.incoming:
            incoming_streets = list(self.incoming[ind])
            schedule = []
            total_sum = 1
            for st in incoming_streets:
                total_sum += street_freq.get(st, 0)
            new_max_inter_sum = max(new_max_inter_sum, total_sum)
            # iterating over a set doesn't gurantee the order
            # sort first to avoid undeterminicity
            incoming_streets.sort(key=lambda x: -street_freq.get(x, 0))
            streets_limit = max(math.ceil(len(incoming_streets)*road_percent/100), 3)
            streets = incoming_streets[:streets_limit]
            # streets.sort(key=lambda x:street_first_car.get(x, MAX_INT)*10+street_freq.get(x, 0)+random.randint(1, 50))
            # streets.sort(key=lambda x:street_freq.get(x, 0)*10)
            streets.sort(key=lambda x:street_first_car.get(x, MAX_INT))
            max_green_light_length = math.ceil(total_sum / max_total_sum * max_max_green_light_length)
            for st in streets:
                value = math.ceil(street_freq.get(st, 0) / total_sum * max_green_light_length)
                if value > 0:
                    schedule.append((st, min(value, self.D)))
            if len(schedule) == 0:
                schedule.append((streets[0], 1))
            sol[ind] = schedule
        self.sol = sol
        return sol, new_max_inter_sum

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
            random.shuffle(streets)
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
        for car_i,car in self.vehicles.items():
            cur_street_name = car[0]
            inter = self.streets[cur_street_name].end
            time_to_leave = self._getNextAllowedTime(cur_street_name, 0)
            queued_car = queuedCar(time_to_leave, car_i, 1)
            if cur_street_name not in street_to_queues or len(street_to_queues[cur_street_name])== 0:
                heapq.heappush(first_cars_pq, queued_car)
            street_to_queues[cur_street_name].append(queued_car)

        score = 0
        cars_passed = set()
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_car_path = self.vehicles[cur_car.car_i]
            cur_street_name = cur_car_path[cur_car.path_j-1]
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car_path[cur_car.path_j]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if cur_car.path_j == len(cur_car_path) - 1 and arrival_at_next_inter <= self.D:
                score += F + (D - arrival_at_next_inter)
                cars_passed.add(cur_car.car_i)
            else:
                time_to_leave_next_inter = self._getNextAllowedTime(outgoing_street_name, arrival_at_next_inter)
                queued_car = queuedCar(time_to_leave_next_inter, cur_car.car_i, cur_car.path_j+1)
                if outgoing_street_name not in street_to_queues or len(street_to_queues[outgoing_street_name])== 0:
                    heapq.heappush(first_cars_pq, queued_car)
                street_to_queues[outgoing_street_name].append(queued_car)
            if len(street_to_queues[cur_street_name]) > 0:
                next_car_in_queue = street_to_queues[cur_street_name][0]
                time_to_leave = self._getNextAllowedTime(cur_street_name, max(cur_car.time_to_leave+1, next_car_in_queue.time_to_leave))
                heapq.heappush(first_cars_pq, queuedCar(time_to_leave, next_car_in_queue.car_i, next_car_in_queue.path_j))
        return score, cars_passed

    def simulate(self, D, F):
        # global priority queue storing first car of each intersection ordered by first allowed time to pass
        first_cars_pq = []
        street_to_queues = defaultdict(list)
        street_names_to_return = []
        for car_i,car in self.vehicles.items():
            cur_street_name = car[0]
            inter = self.streets[cur_street_name].end
            time_to_leave = 0
            queued_car = queuedCar(time_to_leave, car_i, 1)
            if cur_street_name not in street_to_queues or len(street_to_queues[cur_street_name])== 0:
                heapq.heappush(first_cars_pq, queued_car)
            street_to_queues[cur_street_name].append(queued_car)

        score = 0
        cars_passed = 0
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_car_path = self.vehicles[cur_car.car_i]
            cur_street_name = cur_car_path[cur_car.path_j-1]
            street_names_to_return.append((cur_street_name, cur_car.time_to_leave))
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car_path[cur_car.path_j]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if cur_car.path_j == len(cur_car_path) - 1 and arrival_at_next_inter <= self.D:
                score += F + (D - arrival_at_next_inter)
                cars_passed += 1
            else:
                time_to_leave_next_inter = arrival_at_next_inter
                queued_car = queuedCar(time_to_leave_next_inter, cur_car.car_i, cur_car.path_j+1)
                if outgoing_street_name not in street_to_queues or len(street_to_queues[outgoing_street_name])== 0:
                    heapq.heappush(first_cars_pq, queued_car)
                street_to_queues[outgoing_street_name].append(queued_car)
            if len(street_to_queues[cur_street_name]) > 0:
                next_car_in_queue = street_to_queues[cur_street_name][0]
                time_to_leave = max(cur_car.time_to_leave+1, next_car_in_queue.time_to_leave)
                heapq.heappush(first_cars_pq, queuedCar(time_to_leave, next_car_in_queue.car_i, next_car_in_queue.path_j))
        return street_names_to_return, score, cars_passed

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

original_vehicles = {}
for index in range(V):
    original_vehicles[index] = [s for s in input().split(" ")][1:]
all_vehicles = set(original_vehicles.keys())

all_time_max_score = 0

def main(output_file):
    global all_time_max_score
    global V
    opt_sol = None
    max_score = -1
    i = 0 
    start = time.time()
    MIN_DROPPING_VEHICLE = 0
    MAX_DROPPING_VEHICLE = V * 180 // 1000
    MAX_ITER = 5000
    MAX_INTER_TOTAL_SUM = 9999999999
    unpassed_cars = set()
    while time.time() - start < 50 and i < MAX_ITER:
        # vehicles_to_drop = MIN_DROPPING_VEHICLE + i % (MAX_DROPPING_VEHICLE - MIN_DROPPING_VEHICLE)
        vehicles_to_drop = random.randint(MIN_DROPPING_VEHICLE, MAX_DROPPING_VEHICLE)
        keeping_road_percent = 61+i%8
        # keeping_road_percent = 100
        # keeping_road_percent = random.randint(59, 72)
        vehicles = copy.deepcopy(original_vehicles)
        for c in list(unpassed_cars)[:vehicles_to_drop]:
            del vehicles[c]

        s = Solution(streets, incoming, outgoing, vehicles, D)
        sim_street_names, abs_max_score, cars_passed = s.simulate(D, F)
        # eprint(i, 'Simuate score', abs_max_score, len(sim_street_names), cars_passed, len(vehicles))
        MAX_MAX_GREEN_LIGHT_LENGTH = 8+i%18
        # MAX_MAX_GREEN_LIGHT_LENGTH = random.randint(6, 26)
        sol,MAX_INTER_TOTAL_SUM=s.get_sim_solution(sim_street_names, MAX_MAX_GREEN_LIGHT_LENGTH, MAX_INTER_TOTAL_SUM, keeping_road_percent)
        s_eval = Solution(streets, incoming, outgoing, original_vehicles, D)
        s_eval.sol = sol
        score,set_cars_passed = s_eval.evaluate(D, F)
        # eprint(i, 'Cur score:', score, 'max wait time:', s_eval.max_wait_time, 'cars passed', len(set_cars_passed), time.time()-start, 'vehicles_to_drop', vehicles_to_drop, MAX_INTER_TOTAL_SUM, MAX_MAX_GREEN_LIGHT_LENGTH, keeping_road_percent)
        if score > max_score:
            eprint('Max score at: ', i, score, 'max wait time:', s_eval.max_wait_time, 'cars passed:', len(set_cars_passed), time.time()-start, 'vehicles_to_drop:', vehicles_to_drop, MAX_INTER_TOTAL_SUM, MAX_MAX_GREEN_LIGHT_LENGTH, keeping_road_percent)
            unpassed_cars = list(all_vehicles.difference(set_cars_passed))
            random.shuffle(unpassed_cars)
            max_score = score
            opt_sol = sol
        i += 1
    all_time_max_score = max(all_time_max_score, max_score)

    # s = Solution(streets, incoming, outgoing, vehicles, D)
    # opt_sol=s.get_opt_solution(9)
    # eprint('Score:', s.evaluate(D, F))
    print(len(opt_sol), file=output_file)
    for key in opt_sol:
        print(key, file=output_file) # intersection index
        signals = opt_sol[key]
        print(len(signals), file=output_file)
        for sig in signals:
            print(' '.join([str(p) for p in sig]), file=output_file)

ind = 0
while ind < 2000:
    output_file = open('e.out'+str(ind), 'w')
    main(output_file)
    eprint('Wrote to ', output_file, all_time_max_score)
    ind += 1
