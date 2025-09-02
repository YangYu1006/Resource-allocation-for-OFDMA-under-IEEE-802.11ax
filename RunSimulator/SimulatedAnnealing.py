import numpy as np
import math
import time
import random

# ============================
# Runtime-configurable PHY/MAC
# ============================
# Default spatial streams (set at runtime if needed)
N_SS = 2
# Default MCS value (set at runtime if needed)
MCS_VALUE = 11
# GI (microseconds)
GI = 3.2

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

# ============================
# PHY rate & CSMA/CA helpers
# ============================
# NOTE: this MCS table is an approximate mapping for 26-tone RU single spatial-stream
# Units: Mbps per single spatial stream for 26-tone RU (approximate)
MCS_RATE_PER_26_SINGLE_SS = {
    0: 1.8, 1: 3.6, 2: 5.4, 3: 7.2, 4: 10.8,
    5: 14.4, 6: 16.2, 7: 18.0, 8: 21.6,
    9: 24.0, 10: 27.0, 11: 30.0
}

def get_phy_rate(mcs_value=MCS_VALUE, nss=N_SS, ru_size=26):
    """
    Return approximate PHY rate in Mbps for given MCS, spatial streams and RU size.
    - base values correspond to 26-tone RU single spatial stream.
    - for 52-tone RU we approximate ~2x 26-tone.
    - for other RU sizes we scale linearly by ru_size/26.
    This function returns Mbps (not bits/us).
    """
    base = MCS_RATE_PER_26_SINGLE_SS.get(mcs_value, MCS_RATE_PER_26_SINGLE_SS[11])
    if ru_size == 26:
        return base * nss
    elif ru_size == 52:
        return base * 2 * nss
    else:
        scale = ru_size / 26.0
        return base * scale * nss

def csma_ca_delay(num_contenders, cwmin=15, slot_time_us=9, difs_us=34):
    """
    Simple CSMA/CA random backoff model returning access delay in microseconds.
    - Each contender picks uniform backoff in [0, cwmin]
    - We take the minimum backoff as the winner's access time (DIFS + slots)
    - If multiple contenders pick the same min slot, we add an extra random backoff to model collision
    This is a simplified model to account for channel access overhead.
    """
    if num_contenders <= 0:
        num_contenders = 1
    backoffs = [random.randint(0, cwmin) for _ in range(num_contenders)]
    min_slots = min(backoffs)
    delay_us = difs_us + min_slots * slot_time_us
    if backoffs.count(min_slots) > 1:
        # collision coarse handling: extra backoff
        extra_slots = random.randint(0, cwmin)
        delay_us += extra_slots * slot_time_us
    return delay_us

# ============================
# Original variables & structures
# ============================
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

# NOTE: modified weight formula denominator from your previous code to a constant 0.7 in your latest revision
while o < len(PacketSize):
    # keep your original weight structure but unchanged except for safe division
    if 0.7 != 0:
        weight = math.ceil(((PacketSize[o]/5100)/0.7) * Expectation * 10) # average rate the packets arrive in buffer in last time slot(10ms) mb/s
    else:
        weight = 1
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
if num_packets > 0:
    ordered_indices = sorted(random.sample(range(num_packets), num_ordered))
else:
    ordered_indices = []

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


    def knapsack_simulated_annealing(weights, values, capacity, initial_temp=1000, final_temp=1, alpha=0.9,
                                     max_iter=100):
        """
        Simulated Annealing for 0-1 Knapsack (26-tone RU)
        - weights: list of packet weights
        - values: list of packet values
        - capacity: RU capacity
        - initial_temp: starting temperature
        - final_temp: ending temperature
        - alpha: cooling rate
        - max_iter: iterations per temperature
        Returns: (best_total_value, selected_indices)
        """
        n = len(weights)
        if n == 0:
            return 0, []

        # Initial solution: random feasible selection
        current = np.random.randint(2, size=n)
        # Ensure feasible
        while sum([current[i] * weights[i] for i in range(n)]) > capacity:
            ones = [i for i in range(n) if current[i] == 1]
            if not ones:
                break
            current[random.choice(ones)] = 0

        def total_value(solution):
            return sum(solution[i] * values[i] for i in range(n))

        def total_weight(solution):
            return sum(solution[i] * weights[i] for i in range(n))

        best = current.copy()
        best_val = total_value(best)
        temp = initial_temp

        while temp > final_temp:
            for _ in range(max_iter):
                # generate neighbor by flipping one bit
                neighbor = current.copy()
                idx = random.randint(0, n - 1)
                neighbor[idx] = 1 - neighbor[idx]

                # keep feasible
                if total_weight(neighbor) <= capacity:
                    delta = total_value(neighbor) - total_value(current)
                    if delta > 0 or random.random() < np.exp(delta / temp):
                        current = neighbor
                        if total_value(current) > best_val:
                            best = current.copy()
                            best_val = total_value(best)
            temp *= alpha

        selected_indices = [i for i in range(n) if best[i] == 1]
        return best_val, selected_indices

    total_value, x = knapsack_simulated_annealing(w_less_than_or_equal_to_26, p1, m1)
    print('Max Value：', total_value)
    print('Packets put into this RU：', x)
    if x:
        numberofusedRU += 1
    PacketSizeinRU1 = [0] * 200
    while l < len(x):
        # be careful with indexing; original code used x[l-1] leading to potential index shift.
        # keep consistent: if x entries are indices in w_less_than_or_equal_to_26 (0-based),
        # but PacketSize is aligned with GeneratedPacketSize slice; keep original pattern but safe-check.
        idx = x[l] if l < len(x) else x[-1]
        # protect index bounds
        if idx < len(PacketSize):
            PacketSizeinRU1[l] = PacketSize[idx]
        else:
            PacketSizeinRU1[l] = 0
        l = l + 1
    TotalPacketSizeinRU1 = sum(PacketSizeinRU1)
    if x:
        l = 0
        while l < len(x):
            idx = x[l]
            # safe-check QueuingTime1 length
            if idx < len(QueuingTime1):
                AllocatedPacketQueuingTime.append(QueuingTime1[idx])
            else:
                AllocatedPacketQueuingTime.append(0)
            if idx < len(PacketSize):
                AllocatedPacketSize.append(PacketSize[idx])
            else:
                AllocatedPacketSize.append(0)
            if idx < len(NumberofAttemptsforeveryUser):
                AllocatedNumberofAttempts.append(NumberofAttemptsforeveryUser[idx])
            else:
                AllocatedNumberofAttempts.append(1)
            l = l + 1

        # sort allocated lists by queuing time (descending for scheduling)
        sortedPacketSizeinThisRU = sort_my_list_based_on_my_list2(AllocatedPacketSize, AllocatedPacketQueuingTime)
        sorted_Attempts = sort_my_list_based_on_my_list2(AllocatedNumberofAttempts, AllocatedPacketQueuingTime)
        sorted_QueuingTime = sorted(AllocatedPacketQueuingTime, reverse=True)
        l = 0
        QueuingTimeforPacketl = 0
        # ========== Queue delay calculation using PHY rate (modified) ==========
        while l < len(sortedPacketSizeinThisRU):
            # assume this is for 26-tone RU (since we are in <=26 bucket)
            rate_mbps = get_phy_rate(mcs_value=MCS_VALUE, nss=N_SS, ru_size=26)  # Mbps
            # transmission time in microseconds: (bytes * 8 bits) / (Mbps)  -> microseconds
            tx_us = (sortedPacketSizeinThisRU[l] * 8) / rate_mbps
            # accumulate queuing time: previous cumulative + this packet attempt contributions
            # keep similar structure to original but use real tx_us
            sorted_QueuingTime[l] = sorted_QueuingTime[l] + QueuingTimeforPacketl
            QueuingTimeforPacketl = QueuingTimeforPacketl + tx_us * AllocatedNumberofAttempts[l] + GI * (AllocatedNumberofAttempts[l] - 1)
            l = l + 1
        l = 0
        print(AllocatedPacketSize)
        while l < len(sortedPacketSizeinThisRU):
            WhichUser = search_and_output_indices(GeneratedPacketSize, sortedPacketSizeinThisRU[l])
            if WhichUser:
                # write back to QueuingTime safely
                idx_u = WhichUser[0] - 1
                if 0 <= idx_u < len(QueuingTime):
                    QueuingTime[idx_u] = sorted_QueuingTime[l]
            l = l + 1
        l = 0
        TransmissiontimeforRU1 = 0
        # ========== Add CSMA/CA access delay before RU transmissions ==========
        # Estimate number of contenders as number of non-zero PacketSize entries excluding index 0
        num_contenders = max(1, len([s for s in PacketSize[1:] if s > 0]))
        csma_delay_us = csma_ca_delay(num_contenders)
        TransmissiontimeforRU1 += csma_delay_us
        # compute per-packet transmission time with attempts using PHY rate
        while l < len(sorted_Attempts):
            rate_mbps = get_phy_rate(mcs_value=MCS_VALUE, nss=N_SS, ru_size=26)
            tx_time_per_attempt_us = (sortedPacketSizeinThisRU[l] * 8) / rate_mbps
            TransmissionTimeforEveryPacket = tx_time_per_attempt_us * sorted_Attempts[l] + GI * (sorted_Attempts[l] - 1)
            TransmissiontimeforRU1 = TransmissiontimeforRU1 + TransmissionTimeforEveryPacket + GI
            l = l + 1
        TransmissionTime.append(TransmissiontimeforRU1)
    print('Transmission time: %.2fμs'%TransmissiontimeforRU1)
    TotalSC = 0
    l = 0
    while l < len(x):
        idx = x[l]
        if idx < len(w_less_than_or_equal_to_26):
            TotalSC = TotalSC + w_less_than_or_equal_to_26[idx]
        l = l + 1
    l = 0
    if TransmissiontimeforRU1 < 5000:
        while l < len(x):
            idx = x[l]
            if idx < len(PacketSize):
                TotalTransmittedPacketSize = PacketSize[idx] + TotalTransmittedPacketSize
            l = l+1
    else:
        TotalTransmittedPacketSize = TotalTransmittedPacketSize + 100

    # remove allocated items (delete by descending order to keep indices valid)
    for i in sorted(x, reverse=True):
        # check bounds before deletion
        if i < len(PacketSize):
            del (PacketSize[i])
        if i < len(p1):
            del (p1[i])
        if i < len(w_less_than_or_equal_to_26):
            del (w_less_than_or_equal_to_26[i])
        if i < len(QueuingTime1):
            del (QueuingTime1[i])
    k = k+1
    x = []
print(w_less_than_or_equal_to_26)

print('Number of used RU: ', numberofusedRU)
print('The rest packets: ', w_greater_than_26)
NumberoftheRest52tonesRUs = 4 - math.ceil(numberofusedRU/2)
print('Total number of available 52-tones RU: ', NumberoftheRest52tonesRUs)
# protective code if TransmissionTime empty
if TransmissionTime:
    TimeforfinishTransmission = max(TransmissionTime)
else:
    TimeforfinishTransmission = 0
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
# avoid division by zero
if TransmissionTimeforAllocatedRU5000:
    Efficiency = sum(TransmissionTimeforAllocatedRU5000) / (len(TransmissionTimeforAllocatedRU5000) * 5000)
else:
    Efficiency = 0.0
runtime = round((end - start)*1000000, 2)
# ensure TotalPacketSize defined (it is)
PacketGenerationRate = TotalPacketSize*200/1048576 if 'TotalPacketSize' in locals() else 0
print('Program running time: %.2f' % runtime)
if TransmissionTime:
    TimeforfinishallTransmission = runtime + max(TransmissionTime)
else:
    TimeforfinishallTransmission = runtime
print('Time for finish all transmission: %.2fμs'%TimeforfinishallTransmission)
AverageThroughput = (TotalTransmittedPacketSize*1000000/1048576)/TimeforfinishallTransmission if TimeforfinishallTransmission>0 else 0.0
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
        # compute actual arrival order by queuing time
        arrival_order = sorted(group, key=lambda x: QueuingTime[x])
        for i, idx in enumerate(arrival_order):
            expected_seq = ordered_packet_map[idx][1]  # expected order
            actual_seq = i  # observed order within this group's arrivals
            R_values.append(abs(actual_seq - expected_seq))
    except Exception:
        continue

average_R = sum(R_values) / len(R_values) if R_values else 0
print("Average R-value for ordered packets: {:.2f}".format(average_R))
exit(0)