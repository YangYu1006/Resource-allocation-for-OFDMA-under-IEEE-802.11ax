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

GeneratedPacketSize = [600, 202]
PacketSize = GeneratedPacketSize[:]
QueuingTime = []
QueuingTime1 = QueuingTime[:]
Rk = []
Rk2 = []
PacketSize.insert(0, 0)
QueuingTime1.insert(0, 0)
w = []
print(len(PacketSize))
TotalPacketSize = sum(PacketSize)
print(TotalPacketSize)
PacketGenerationRate = TotalPacketSize*200/1048576
BufferSize = 32000000   # Buffer size is 32Mb
if PacketGenerationRate < 1280000:
    RUallocationInterval = BufferSize / PacketGenerationRate
else:
    RUallocationInterval = 25

o = 0
BufferOccupancy = []
TransmissionTimeforEveryPacket = []

while o < len(PacketSize):
    weight = math.ceil(((PacketSize[o]/5100)/(3.5 * RUallocationInterval)) * Expectation * 10) # average rate the packets arrive in buffer in last time slot(10ms) mb/s
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
o = 1
numberofusedRU = 0
p1 = [0]  # value for a packet in 26-tones RU
p2 = [0]  # value for a packet in 26-tones RU
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

Expected_order = []

for group in ordered_groups:
    group_expected = list(range(len(group)))  # order start from 0
    Expected_order.extend(group_expected)
TotalnumberofEfficientuseofSCsin26RUs = 0
# Record an index of packets that have already been allocated to avoid duplication.
used_packet_indices = set()

# Building knapsack inputs (packet group-aware)
def prepare_knapsack_items(w, p, ordered_groups, used_indices):
    items = []
    added = set()
    for group in ordered_groups:
        if any(idx+1 in used_indices for idx in group):
            continue
        weight = sum(w[idx+1] for idx in group)
        value = sum(p[idx+1] for idx in group)
        items.append({
            "indices": [idx+1 for idx in group],
            "weight": weight,
            "value": value,
            "is_ordered": True
        })
        added.update(idx+1 for idx in group)
    for i in range(1, len(w)):
        if i not in added and i not in used_indices:
            items.append({
                "indices": [i],
                "weight": w[i],
                "value": p[i],
                "is_ordered": False
            })
    return items

while k < 9:
    n = len(w_less_than_or_equal_to_26) - 1
    v = 0
    optp = [[0 for col in range(m1 + 1)] for raw in range(n + 1)]
    l = 0
    AllocatedPacketQueuingTime = []
    AllocatedPacketSize = []
    AllocatedNumberofAttempts = []


    def knapsack_with_groups(items, capacity):
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        keep = [[[] for _ in range(capacity + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            wt = items[i - 1]['weight']
            val = items[i - 1]['value']
            idxs = items[i - 1]['indices']
            for j in range(capacity + 1):
                if j >= wt:
                    if dp[i - 1][j - wt] + val > dp[i - 1][j]:
                        dp[i][j] = dp[i - 1][j - wt] + val
                        keep[i][j] = keep[i - 1][j - wt] + [idxs]
                    else:
                        dp[i][j] = dp[i - 1][j]
                        keep[i][j] = keep[i - 1][j][:]
                else:
                    dp[i][j] = dp[i - 1][j]
                    keep[i][j] = keep[i - 1][j][:]
        return dp[n][capacity], keep[n][capacity]


    items = prepare_knapsack_items(w_less_than_or_equal_to_26, p1, ordered_groups, used_packet_indices)
    max_val, selected_packet_groups = knapsack_with_groups(items, m1)

    print('Max Value：', max_val)
    print('Packets put into this RU：', selected_packet_groups)

    # Flatten group list to [i1, i2, i3, ...]
    x = [i for group in selected_packet_groups for i in group]
    used_packet_indices.update(x)

    if x:
        numberofusedRU += 1
    PacketSizeinRU1 = [0] * 200
    while l < len(x):
        PacketSizeinRU1[l] = PacketSize[x[l]]
        l = l + 1
    TotalPacketSizeinRU1 = sum(PacketSizeinRU1)
    if x:
        l = 0
        while l < len(x):
            AllocatedPacketQueuingTime.append(QueuingTime1[x[l]])
            AllocatedPacketSize.append(PacketSize[x[l]])
            AllocatedNumberofAttempts.append(x[l])
            l = l + 1


        def sort_preserving_group_order(packet_indices, queuing_times, ordered_packet_map):
            group_map = {}
            non_group = []
            for idx in packet_indices:
                real_idx = idx - 1
                if real_idx in ordered_packet_map:
                    gid = ordered_packet_map[real_idx][0]
                    if gid not in group_map:
                        group_map[gid] = []
                    group_map[gid].append(idx)
                else:
                    non_group.append(idx)

            # sorting
            sorted_groups = sorted(group_map.items(), key=lambda g: min(queuing_times[i] for i in g[1]))
            result = []
            for _, group in sorted_groups:
                group_sorted = sorted(group, key=lambda i: ordered_packet_map[i - 1][1])
                result.extend(group_sorted)

            # Ungrouped packets continue in descending order by queuing time.
            non_group_sorted = sorted(non_group, key=lambda i: queuing_times[i], reverse=True)
            result.extend(non_group_sorted)
            return result


        sorted_packet_indices = sort_preserving_group_order(AllocatedNumberofAttempts, QueuingTime1, ordered_packet_map)

        sortedPacketSizeinThisRU = [PacketSize[i] for i in sorted_packet_indices]
        sorted_Attempts = [NumberofAttemptsforeveryUser[i] for i in sorted_packet_indices]
        sorted_QueuingTime = [QueuingTime1[i] for i in sorted_packet_indices]

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
    for idx in sorted(x, reverse=True):
        del PacketSize[idx]
        del p1[idx]
        del w_less_than_or_equal_to_26[idx]
        del QueuingTime1[idx]
    k = k+1
    x = []
print(w_less_than_or_equal_to_26)
l = 0
while l < len(w_less_than_or_equal_to_26):
    w_greater_than_26.append(w_less_than_or_equal_to_26[l])
    l = l + 1
print('Number of used RU: ', numberofusedRU)
print('The rest packets: ', w_greater_than_26)
NumberoftheRest52tonesRUs = 4 - math.ceil(numberofusedRU/2)
print('Total number of available 52-tones RU: ', NumberoftheRest52tonesRUs)
TimeforfinishTransmission = max(TransmissionTime)
print(TransmissionTime)
print('Total Transmissiontime: %.2fμs'%TimeforfinishTransmission)
o = 0
m2 = 520  # capacity for 52-tones RU
o = 1
while o < len(w_greater_than_26):
    valueof1packet = w_greater_than_26[o]
    p2.append(valueof1packet)
    o = o + 1
print('Value for packets bigger than 26: ', p2)
o = 0
k = 0
x = []
y = 0
z = 1
TotalnumberofEfficientuseofSCsin52RUs = 0
numberofused52RU = 0
while k < NumberoftheRest52tonesRUs:
    n = len(w_greater_than_26) - 1
    v = 0
    optp = [[0 for col in range(m2 + 1)] for raw in range(n + 1)]
    l = 0
    def knapsack_dynamic(w_greater_than_26, p2, n, m2, x):
        for i in range(1, n + 1):
            for j in range(1, m2 + 1):
                if (j >= w_greater_than_26[i]):
                    optp[i][j] = max(optp[i - 1][j],
                                     optp[i - 1][j - w[i]] + p2[i])
                else:
                    optp[i][j] = optp[i - 1][j]
                    j = m2
        for i in range(n, 0, -1):
            if optp[i][j] > optp[i - 1][j]:
                x.append(i)
                j = j - w_greater_than_26[i]

            # return max value which is the number in the last row and last line of the table
        v = optp[n][m1]
        return v
    print('Max Value：', knapsack_dynamic(w_greater_than_26, p2, n, m2, x))
    print('Packets put into this RU：', x)
    if x:
        numberofused52RU += 1
    l = 0
    while l < len(x):
        TotalTransmittedPacketSize = PacketSize[x[l]] + TotalTransmittedPacketSize
        del(p2[x[l]])
        del(w_greater_than_26[x[l]])
        l = l+1
    k = k+1
    x = []
print('Number of used 52-tones RU: ', numberofused52RU)
TotalusedSCs = numberofusedRU * 26 + numberofused52RU * 52
end = time.time()
TransmissionTimeforAllocatedRU = [x for x in TransmissionTime if x > 0]
TransmissionTimeforAllocatedRU5000 = [x if x <= 5000 else 4900 for x in TransmissionTimeforAllocatedRU]
print('Transmission time for every RU which has been allocated: ', TransmissionTimeforAllocatedRU5000)
Efficiency = sum(TransmissionTimeforAllocatedRU5000) / (len(TransmissionTimeforAllocatedRU5000) * 5000)
runtime = round((end - start)*1000000, 2)
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
Actual_order = []
Expected_order_pointer = 0

for group in ordered_groups:
    arrival_order = sorted(group, key=lambda x: QueuingTime[x])  # actual order
    for actual_seq, pkt_id in enumerate(arrival_order):
        expected_seq = Expected_order[Expected_order_pointer]
        Expected_order_pointer += 1

        R_values.append(abs(actual_seq - expected_seq))
        Actual_order.append(actual_seq)

print('Expected order: ', Expected_order)
print('Actual order: ', Actual_order)
average_R = sum(R_values) / len(R_values) if R_values else 0
print("Average R-value for ordered packets: {:.2f}".format(average_R))
exit(0)
