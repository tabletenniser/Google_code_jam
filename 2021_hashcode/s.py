import random
import sys
import math
import time
import heapq
from collections import namedtuple,defaultdict
import copy

MAX_INT = 10000000
MAX_MAX_GREEN_LIGHT_LENGTH = 12
DESIRED_IND_OFFSET = random.randint(0,0)
MIN_DROPPING_VEHICLE = 0
MAX_DROPPING_VEHICLE = 160
QUEUE_THRESHOLD = 200
QUEUE_DIVIDER = 200
FIRST_X_PERCENT_QUEUE = 100
QUEUED_STREETS = {}
LONG_WAIT_DEBUG_THRESHOLD = 220
FIRST_X_PERCENT_LONG_WAIT = 30
# DEBUGGING_STREETS = {'bei-i', 'i-bb', 'bb-fbb', 'fbb-bjjc'}
DEBUGGING_STREETS = {}

queuedCar = namedtuple('queuedCar', ['time_to_leave','car_i', 'path_j'])
Street = namedtuple('Street', ['name', 'begin', 'end', 'length'])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Solution(object):
    def __init__(self, streets, incoming, vehicles, D, max_green_light):
        self.max_green_light = max_green_light
        self.streets = streets # {name: (name, begin, end, l)}
        self.D = D  # simulation duration
        vehicle_path_length_pair = []
        self.max_street_length = max([s.length for s in self.streets.values()])
        self.vehicles = vehicles
        self.street_frequency = {} # {name_str: frequency_int}
        for _,v in self.vehicles.items():
            for s in v[:-1]:
                self.street_frequency[s] = self.street_frequency.get(s, 0)+1
        self.max_wait_time = 0 # metric: max wait for bad order
        self.incoming = copy.deepcopy(incoming) # {interection: {streets}}
        self.inter_total_freq = {} # {intersection: freq_int}
        for inter in self.incoming.keys():
            self.incoming[inter] = list(filter(lambda x: x in self.street_frequency and self.street_frequency[x] > 0, self.incoming[inter]))
            self.inter_total_freq[inter] = 0
            for st in self.incoming[inter]:
                self.inter_total_freq[inter] += self.street_frequency[st]
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
        if incoming_street in DEBUGGING_STREETS:
            eprint(incoming_street, ' evaluate start time: ', earliest_time)
        inter = self.streets[incoming_street].end
        if inter not in self.sol:
            return MAX_INT
        schedule = self.sol[inter]
        cycle_time = sum([s[1] for s in schedule if s is not None])
        assert cycle_time != 0, incoming_street + str(schedule)+str(self.street_frequency)
        cur_sim_time = earliest_time - earliest_time % cycle_time
        street_index = 0
        while cur_sim_time < earliest_time:
            cur_sim_time += schedule[street_index][1]
            if cur_sim_time > earliest_time and schedule[street_index][0] == incoming_street:
                return earliest_time

            street_index = (street_index + 1) % len(schedule)
        i = 0
        assert schedule[street_index] is not None, str(schedule)+' must not have none'
        while schedule[street_index][0] != incoming_street:
            cur_sim_time += schedule[street_index][1]
            street_index = (street_index + 1) % len(schedule)
            assert schedule[street_index] is not None, str(schedule)+' must not have none'
            i += 1
            if i > len(schedule):
                return MAX_INT
        cur_wait_time = cur_sim_time - earliest_time
        # if cur_wait_time > LONG_WAIT_DEBUG_THRESHOLD:
        #     eprint('Long evaluate wait:', cur_wait_time, incoming_street, earliest_time, cur_sim_time)
        self.max_wait_time = max(self.max_wait_time, cur_wait_time)
        if incoming_street in DEBUGGING_STREETS:
            eprint(incoming_street, ' evaluate returned time: ', cur_sim_time)
        return cur_sim_time

    def evaluate(self, F):
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
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < self.D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_car_path = self.vehicles[cur_car.car_i]
            cur_street_name = cur_car_path[cur_car.path_j-1]
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car_path[cur_car.path_j]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if cur_car.path_j == len(cur_car_path) - 1 and arrival_at_next_inter <= self.D:
                score += F + (self.D - arrival_at_next_inter)
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

    def _findNextAllowedTime(self, incoming_street, earliest_time):
        if incoming_street in DEBUGGING_STREETS:
            eprint(incoming_street, ' simulate start time: ', earliest_time)
        inter = self.streets[incoming_street].end
        num_strts = len(self.incoming[inter])
        if num_strts == 0:
            return MAX_INT
        assert num_strts > 0, incoming_street + inter + str(self.incoming[inter])
        if inter not in self.sol:
            self.sol[inter] = [None for _ in range(num_strts)]
        schedule = self.sol[inter]
        scheduled_streets = {s[0] for s in schedule if s is not None}
        if incoming_street not in scheduled_streets:
            offset = 0
            if incoming_street in self.prev_long_wait_streets:
                offset = self.prev_long_wait_streets[incoming_street][0]
            desired_ind= (earliest_time - offset + DESIRED_IND_OFFSET) % num_strts
            while schedule[desired_ind] is not None:
                desired_ind = (desired_ind+ 1) % num_strts
            w = math.ceil(self.street_frequency.get(incoming_street, 0) / self.inter_total_freq[inter] * self.max_green_light)
            # w = 1 if incoming_street not in self.prev_long_queue_streets else self.prev_long_queue_streets[incoming_street][0] // QUEUE_DIVIDER
            schedule[desired_ind] = (incoming_street, w)
        # TODO: Make this work when not all streets have 1. If not-1 weight gets inserted, try move all subsequent indices if possible.
        cur_sim_time = earliest_time - earliest_time % num_strts
        street_index = 0
        while cur_sim_time < earliest_time:
            cur_sim_time += 1
            if cur_sim_time > earliest_time and schedule[street_index][0] == incoming_street:
                return earliest_time

            street_index = (street_index + 1) % len(schedule)
        i = 0
        while schedule[street_index] is None or schedule[street_index][0] != incoming_street:
            cur_sim_time += 1
            street_index = (street_index + 1) % len(schedule)
            i += 1
            if i > len(schedule):
                return MAX_INT
        cur_wait_time = cur_sim_time - earliest_time
        if cur_wait_time > LONG_WAIT_DEBUG_THRESHOLD and incoming_street not in self.long_wait_streets and earliest_time < self.D /100* FIRST_X_PERCENT_LONG_WAIT:
            self.long_wait_streets[incoming_street] = (cur_wait_time, earliest_time)
            # eprint('Long simulate wait:', cur_wait_time, incoming_street, earliest_time, cur_sim_time)
        self.max_wait_time = max(self.max_wait_time, cur_wait_time)
        if incoming_street in DEBUGGING_STREETS:
            eprint(incoming_street, ' simulate returned time: ', cur_sim_time)
        return cur_sim_time

    # TODO: Update this to return: 1) # of cars passed; 2) congested streets; 3) streets with long wait due to bad order
    def simulate(self, F, long_wait_streets, long_queue_streets):
        self.prev_long_wait_streets = long_wait_streets
        self.prev_long_queue_streets = long_queue_streets
        self.long_wait_streets = {}
        self.long_queue_streets = {}
        self.sol = {}
        # global priority queue storing first car of each intersection ordered by first allowed time to pass
        first_cars_pq = []
        street_to_queues = defaultdict(list)
        for car_i,car in self.vehicles.items():
            cur_street_name = car[0]
            inter = self.streets[cur_street_name].end
            time_to_leave = self._findNextAllowedTime(cur_street_name, 0)
            queued_car = queuedCar(time_to_leave, car_i, 1)
            if cur_street_name not in street_to_queues or len(street_to_queues[cur_street_name])== 0:
                heapq.heappush(first_cars_pq, queued_car)
            street_to_queues[cur_street_name].append(queued_car)

        score = 0
        cars_passed = set()
        while len(first_cars_pq) > 0 and first_cars_pq[0].time_to_leave < self.D:
            cur_car = heapq.heappop(first_cars_pq)
            cur_car_path = self.vehicles[cur_car.car_i]
            cur_street_name = cur_car_path[cur_car.path_j-1]
            street_to_queues[cur_street_name].pop(0)
            outgoing_street_name = cur_car_path[cur_car.path_j]
            arrival_at_next_inter = cur_car.time_to_leave + self.streets[outgoing_street_name].length
            if cur_car.path_j == len(cur_car_path) - 1 and arrival_at_next_inter <= self.D:
                score += F + (self.D - arrival_at_next_inter)
                cars_passed.add(cur_car.car_i)
            else:
                time_to_leave_next_inter = self._findNextAllowedTime(outgoing_street_name, arrival_at_next_inter)
                queued_car = queuedCar(time_to_leave_next_inter, cur_car.car_i, cur_car.path_j+1)
                if outgoing_street_name not in street_to_queues or len(street_to_queues[outgoing_street_name])== 0:
                    heapq.heappush(first_cars_pq, queued_car)
                street_to_queues[outgoing_street_name].append(queued_car)
            queue_length = len(street_to_queues[cur_street_name])
            if queue_length> 0:
                next_car_in_queue = street_to_queues[cur_street_name][0]
                time_to_leave = self._findNextAllowedTime(cur_street_name, max(cur_car.time_to_leave+1, next_car_in_queue.time_to_leave))
                if time_to_leave > cur_car.time_to_leave + 1 and queue_length >= QUEUE_THRESHOLD and cur_street_name not in self.long_queue_streets and cur_car.time_to_leave < self.D / 100 * FIRST_X_PERCENT_QUEUE:
                    # eprint(cur_street_name, " has queue lenth of ", queue_length, " at time: ", cur_car.time_to_leave)
                    self.long_queue_streets[cur_street_name] = (queue_length, cur_car.time_to_leave)
                heapq.heappush(first_cars_pq, queuedCar(time_to_leave, next_car_in_queue.car_i, next_car_in_queue.path_j))
        return score, cars_passed

D, I, S, V, F = [int(s) for s in input().strip().split(" ")]
streets = {}
incoming = {}
for index in range(S):
    B, E, name, length = [s for s in input().split(" ")]
    inter = incoming.get(E, set())
    inter.add(name)
    incoming[E] = inter
    streets[name] = Street(name, B, E, int(length))

original_vehicles = {}
for index in range(V):
    original_vehicles[index] = [s for s in input().split(" ")][1:]

opt_sol = None
max_score = -1
i = 0
# s = Solution(streets, incoming, original_vehicles, D)
# eprint('Abs max score', abs_max_score, cars_passed, len(original_vehicles), sim_street_names)
start = time.time()
MAX_ITER = 1000
all_vehicles = set(original_vehicles.keys())
while time.time() - start < 1200 and i < MAX_ITER:
    j = 0
    vehicles_to_drop = MIN_DROPPING_VEHICLE + i % (MAX_DROPPING_VEHICLE - MIN_DROPPING_VEHICLE)
    max_green_light = 1+i % MAX_MAX_GREEN_LIGHT_LENGTH
    DESIRED_IND_OFFSET = random.randint(max_green_light-1, max_green_light+3)
    prev_long_wait_streets = {}
    prev_long_queue_streets = {}
    vehicles = copy.deepcopy(original_vehicles)
    while j < 2:
        s = Solution(streets, incoming, vehicles, D, max_green_light)
        score, cars_passed = s.simulate(F, prev_long_wait_streets, prev_long_queue_streets)
        eprint(i, 'Simuate score ', j, score, s.max_wait_time, len(cars_passed), s.long_wait_streets, s.long_queue_streets)
        prev_long_queue_streets = s.long_queue_streets
        prev_long_wait_streets = s.long_wait_streets
        unpassed_cars = all_vehicles.difference(cars_passed)
        # eprint(unpassed_cars)
        # eprint(vehicles.keys())
        if j == 0:
            for c in list(unpassed_cars)[:vehicles_to_drop]:
                del vehicles[c]
        j += 1
    max_green_light_length = 1
    # sol=s.get_opt_solution(max_green_light_length)
    # sol=s.get_sim_solution(sim_street_names, max_green_light_length, 0)
    # Filter None streets because there can be streets that didn't
    # arrive have cars for input but didn't arrive before end of
    # simulation.
    for st in s.sol:
        s.sol[st] = list(filter(lambda x: x is not None, s.sol[st]))
    sol = s.sol
    score,cars_passed = s.evaluate(F)
    # eprint(i, 'Cur score:', score, 'max wait time:', s.max_wait_time, 'cars passed', cars_passed, time.time()-start, 'max_green_light_length', max_green_light_length)
    if score > max_score:
        eprint('Max score at: ', i, score, '; max wait time:', s.max_wait_time, '; cars passed:', len(cars_passed), time.time()-start, 'max_green_light: ', max_green_light, 'vehicles:', len(vehicles))
        max_score = score
        opt_sol = sol
    i += 1

# s = Solution(streets, incoming, vehicles, D)
# opt_sol=s.get_opt_solution(9)
# eprint('Score:', s.evaluate(F))
print(len(opt_sol))
for key in opt_sol:
    print(key) # intersection index
    signals = opt_sol[key]
    print(len(signals))
    for sig in signals:
        print(' '.join([str(p) for p in sig]))
