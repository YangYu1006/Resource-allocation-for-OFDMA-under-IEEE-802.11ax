import numpy as np
import math
import time
import random

# Number of Spacial Streams: 2
# 20MHz channel
# MCS value:11
# GI: 3.2 microseconds
# Retransmission rate: 50%

def generate_transmission_statistics(retransmission_rate):
    max_attempts = 5
    fail_prob = retransmission_rate
    success_prob = 1 - fail_prob

    attempts = np.arange(1, max_attempts + 1)
    probabilities = []

    for k in range(1, max_attempts):
        prob = (fail_prob ** (k - 1)) * success_prob
        probabilities.append(prob)

    prob_last = 1 - sum(probabilities)
    probabilities.append(prob_last)

    return attempts, np.round(probabilities, 6)

retransmission_rate = 0.2  # retransmission rate
values, probabilities = generate_transmission_statistics(retransmission_rate)
start = time.time()
a = 0
Expectation = 0
while a < len(values):
    Expectation = probabilities[a] * values[a] + Expectation
    a = a + 1

def search_and_output_indices(arr, target):
    matching_indices = [i for i, x in enumerate(arr) if x == target]
    return matching_indices

def sort_my_list_based_on_my_list2(my_list, my_list2):
    combined = list(zip(my_list, my_list2))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_my_list = [x[0] for x in sorted_combined]
    return sorted_my_list

def generate_random_with_probability(probabilities, values):
    if len(probabilities) != len(values):
        raise ValueError("Length of Possibility and number of attempts should be equal.")

    total_prob = sum(probabilities)
    probabilities = [p / total_prob for p in probabilities]
    rand = random.random()

    cumulative_prob = 0
    for i, prob in enumerate(probabilities):
        cumulative_prob += prob
        if rand < cumulative_prob:
            return values[i]

GeneratedPacketSize = []
PacketSize = GeneratedPacketSize[:]
QueuingTime = []
QueuingTime1 = QueuingTime[:]
Rk = []
Rk2 = []

w = []
print(len(PacketSize))
TotalPacketSize = sum(PacketSize)
print(TotalPacketSize)
BufferSize = 32000000   # Buffer size is 32Mb
o = 0
BufferOccupancy = []
TransmissionTimeforEveryPacket = []

while o < len(PacketSize):
    weight = math.ceil(((PacketSize[o]/5100)/0.7) * Expectation * 10) # average rate the packets arrive in buffer in last time slot(10ms) mb/s
    w.append(weight)
    o = o+1
print(w)
w_less_than_or_equal_to_26 = [x for x in w if x <= 260]
w_greater_than_26 = [x for x in w if x > 260]
print(w_greater_than_26)
print(w_less_than_or_equal_to_26)
m1 = 260  # capacity for 26-tones RU
if w_greater_than_26:
    RestSCin52tonesRU = 520 - min(w_greater_than_26)
o = 0
numberofusedRU = 0
p1 = []  # value for a packet in 26-tones RU
p2 = []  # value for a packet in 26-tones RU
while o < len(w_less_than_or_equal_to_26):
    valueof1packet = w_less_than_or_equal_to_26[o]
    p1.append(valueof1packet)
    o = o+1
print('Value for packet less than 26: ', p1)
o = 0
TransmissionTime = []
TotalTransmittedPacketSize = 0
k = 0
x = []
y = 0
z = 1
NumberofAttemptsforeveryUser = []
l = 0
while l < len(GeneratedPacketSize):
    NumberofAttempts = generate_random_with_probability(probabilities, values)
    NumberofAttemptsforeveryUser.append(NumberofAttempts)
    l = l + 1
NumberofAttemptsforeveryUser.insert(0, 0)
print('Number of attempts of every user: ', NumberofAttemptsforeveryUser)
#  GeneratedPacketSize
num_packets = len(GeneratedPacketSize)
num_ordered = int(0.7 * num_packets)

# 70% packets are ordered packets
ordered_indices = sorted(random.sample(range(num_packets), num_ordered))


ordered_groups = []
i = 0
while i < len(ordered_indices):
    group_size = random.randint(5, 10)
    group = ordered_indices[i:i+group_size]
    if len(group) >= 2:
        ordered_groups.append(group)
    i += group_size

# packet_index -> (group_id, seq_in_group)
ordered_packet_map = {}
group_id = 0
for group in ordered_groups:
    for seq, idx in enumerate(group):
        ordered_packet_map[idx] = (group_id, seq)
    group_id += 1

TotalnumberofEfficientuseofSCsin26RUs = 0
while k < 9:
    n = len(w_less_than_or_equal_to_26) - 1
    v = 0
    l = 0
    AllocatedPacketQueuingTime = []
    AllocatedPacketSize = []
    AllocatedNumberofAttempts = []


    def knapsack_simulated_annealing(weights, values, capacity, max_iter=5000, initial_temp=100.0, cooling_rate=0.995):
        n = len(weights)
        if n == 0:
            return 0, []

        # 初始化解（随机0-1向量）
        current_solution = np.random.randint(2, size=n)

        def evaluate(solution):
            total_weight = sum(solution[i] * weights[i] for i in range(n))
            total_value = sum(solution[i] * values[i] for i in range(n))
            if total_weight > capacity:
                return 0
            return total_value

        current_value = evaluate(current_solution)
        best_solution = current_solution.copy()
        best_value = current_value
        T = initial_temp

        for _ in range(max_iter):
            # 生成邻居：随机翻转一个bit
            neighbor = current_solution.copy()
            idx = random.randint(0, n - 1)
            neighbor[idx] = 1 - neighbor[idx]
            neighbor_value = evaluate(neighbor)

            delta = neighbor_value - current_value
            if delta > 0 or random.random() < math.exp(delta / T):
                current_solution = neighbor
                current_value = neighbor_value
                if current_value > best_value:
                    best_solution = current_solution.copy()
                    best_value = current_value
            T *= cooling_rate
            if T < 1e-6:
                break

        selected_indices = [i for i in range(n) if best_solution[i] == 1]
        return best_value, selected_indices

    total_value, x = knapsack_simulated_annealing(w_less_than_or_equal_to_26, p1, m1)
    print('Max Value：', total_value)
    print('Packets put into this RU：', x)
    if x:
        numberofusedRU += 1
    PacketSizeinRU1 = [0] * 200
    while l < len(x):
        PacketSizeinRU1[l] = PacketSize[x[l-1]]
        l = l + 1
    TotalPacketSizeinRU1 = sum(PacketSizeinRU1)
    if x:
        l = 0
        while l < len(x):
            AllocatedPacketQueuingTime.append(QueuingTime1[x[l]])
            AllocatedPacketSize.append(PacketSize[x[l]])
            AllocatedNumberofAttempts.append(NumberofAttemptsforeveryUser[x[l]])
            l = l + 1
        sortedPacketSizeinThisRU = sort_my_list_based_on_my_list2(AllocatedPacketSize, AllocatedPacketQueuingTime)
        sorted_Attempts = sort_my_list_based_on_my_list2(AllocatedNumberofAttempts, AllocatedPacketQueuingTime)
        sorted_QueuingTime = sorted(AllocatedPacketQueuingTime, reverse=True)
        l = 0
        QueuingTimeforPacketl = 0
        while l < len(sortedPacketSizeinThisRU):
            sorted_QueuingTime[l] = sorted_QueuingTime[l] + QueuingTimeforPacketl
            QueuingTimeforPacketl = QueuingTimeforPacketl + ((sortedPacketSizeinThisRU[l] / 18.8) + 3.2) * AllocatedNumberofAttempts[l] + 3.2 * (AllocatedNumberofAttempts[l] - 1)
            l = l + 1
        l = 0
        print(AllocatedPacketSize)
        while l < len(sortedPacketSizeinThisRU):
            WhichUser = search_and_output_indices(GeneratedPacketSize, sortedPacketSizeinThisRU[l])
            QueuingTime[WhichUser[0] - 1] = sorted_QueuingTime[l]
            l = l + 1
        l = 0
        TransmissiontimeforRU1 = 0
        while l < len(sorted_Attempts):
            TransmissionTimeforEveryPacket = (sortedPacketSizeinThisRU[l] / 18.8) * sorted_Attempts[l] + 3.2 * (sorted_Attempts[l] - 1)
            TransmissiontimeforRU1 = TransmissiontimeforRU1 + TransmissionTimeforEveryPacket + 3.2
            l = l + 1
        TransmissionTime.append(TransmissiontimeforRU1)
    print('Transmission time: %.2fμs'%TransmissiontimeforRU1)
    TotalSC = 0
    l = 0
    while l < len(x):
        TotalSC = TotalSC + w_less_than_or_equal_to_26[x[l]]
        l = l + 1
    l = 0
    if TransmissiontimeforRU1 < 5000:
        while l < len(x):
            TotalTransmittedPacketSize = PacketSize[x[l]] + TotalTransmittedPacketSize
            l = l+1
    else:
        TotalTransmittedPacketSize = TotalTransmittedPacketSize + 100

    for i in sorted(x, reverse=True):
        del (PacketSize[i])
        del (p1[i])
        del (w_less_than_or_equal_to_26[i])
        del (QueuingTime1[i])
        l = l + 1
    k = k+1
    x = []
print(w_less_than_or_equal_to_26)

print('Number of used RU: ', numberofusedRU)
print('The rest packets: ', w_greater_than_26)
NumberoftheRest52tonesRUs = 4 - math.ceil(numberofusedRU/2)
print('Total number of available 52-tones RU: ', NumberoftheRest52tonesRUs)
TimeforfinishTransmission = max(TransmissionTime)
print(TransmissionTime)
print('Total Transmissiontime: %.2fμs'%TimeforfinishTransmission)

print('Value for packets bigger than 26: ', p2)

TotalnumberofEfficientuseofSCsin52RUs = 0
numberofused52RU = 0

TotalusedSCs = numberofusedRU * 26 + numberofused52RU * 52
end = time.time()
TransmissionTimeforAllocatedRU = [x for x in TransmissionTime if x > 0]
TransmissionTimeforAllocatedRU5000 = [x if x <= 5000 else 4900 for x in TransmissionTimeforAllocatedRU]
print('Transmission time for every RU which has been allocated: ', TransmissionTimeforAllocatedRU5000)
Efficiency = sum(TransmissionTimeforAllocatedRU5000) / (len(TransmissionTimeforAllocatedRU5000) * 5000)
runtime = round((end - start)*1000000, 2)
PacketGenerationRate = TotalPacketSize*200/1048576
print('Program running time: %.2f' % runtime)
TimeforfinishallTransmission = runtime + max(TransmissionTime)
print('Time for finish all transmission: %.2fμs'%TimeforfinishallTransmission)
AverageThroughput = (TotalTransmittedPacketSize*1000000/1048576)/TimeforfinishallTransmission
print('Total transmitted packet size: ', TotalTransmittedPacketSize)
print('Average throughput: %.2fMb/s'%AverageThroughput)
print('Packet Generation rate: %.2fMb/s'%PacketGenerationRate)
print('Efficiency: %.2f'%Efficiency)
print('Queuing time: ', QueuingTime)
# R-value
R_values = []

# ordered_groups is a set of two-dimensional lists, each representing the index of a batch of packets that should arrive in sequence
# ordered_packet_map is a dict that records the deserved sequential number of each ordered packet within the group it belongs to

for group in ordered_groups:
    try:
        # real order
        arrival_order = sorted(group, key=lambda x: QueuingTime[x])

        # R-value calculation
        for i, idx in enumerate(arrival_order):
            expected_seq = ordered_packet_map[idx][1]  # expected order
            actual_seq = i  # real order
            R_values.append(abs(actual_seq - expected_seq))  # 加入R值
    except IndexError:
        continue


average_R = sum(R_values) / len(R_values) if R_values else 0
print("Average R-value for ordered packets: {:.2f}".format(average_R))
exit(0)