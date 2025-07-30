import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import pareto, poisson

# 定义仿真参数
NUM_SUBCARRIERS = 26  # 每个资源单元的子载波数量
SIMULATION_TIME = 5000  # 仿真总时间（毫秒）
PACKET_GEN_INTERVAL = 5  # 每5毫秒生成一次包
RESET_INTERVAL = 50  # 每50毫秒重置平均等待时间
USER_COUNTS = range(2, 71)  # 仿真用户数量从2到70
RETRANSMISSION_RATES = [0, 0.2, 0.5]  # 重传率
NUM_CYCLES = SIMULATION_TIME // PACKET_GEN_INTERVAL  # 分配周期数

# 数据包大小分布（Pareto或泊松）
def generate_packet_size(dist_type='pareto'):
    if dist_type == 'pareto':
        # Pareto分布, 参数可调整
        return int(pareto.rvs(2, size=1) * 50)
    elif dist_type == 'poisson':
        # 泊松分布, 参数可调整
        return poisson.rvs(5) * 50
    return random.randint(50, 1000)

# 每个用户生成5到10个数据包
def generate_packets(num_users):
    packets = {}
    for user in range(num_users):
        num_packets = random.randint(5, 10)
        packets[user] = [generate_packet_size('pareto') for _ in range(num_packets)]
    return packets

# 背包问题动态规划分配
def allocate_packets(packets, num_subcarriers):
    # 假设我们使用动态规划进行背包问题求解，来分配子载波。
    allocation = {}
    for user, user_packets in packets.items():
        allocation[user] = []
        remaining_carriers = num_subcarriers
        for packet in user_packets:
            if packet <= remaining_carriers:
                allocation[user].append(packet)
                remaining_carriers -= packet
    return allocation

# 计算R Value统计错乱程度
def calculate_r_value(user_packets):
    """
    计算每个用户的R Value，统计包到达顺序的错乱程度。
    使用逆序数（Inversion Count）作为衡量标准。
    每个用户的R-value除以该用户的数据包数量进行归一化。
    """
    total_r_value = 0
    total_users = len(user_packets)

    for user, packets in user_packets.items():
        n = len(packets)
        if n > 1:  # 如果用户有多个包，才计算逆序数
            user_r_value = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if packets[i] > packets[j]:
                        user_r_value += 1  # 发现逆序，增加 user_r_value

            # 将用户的R-value除以该用户的包数量
            total_r_value += user_r_value / n

    # 返回所有用户R-value的总和，除以用户数量
    if total_users > 0:
        return total_r_value / total_users
    else:
        return 0
# 主仿真函数
# 主仿真函数
def run_simulation():
    results = {}  # 存储每种重传率下的结果
    for retransmission_rate in RETRANSMISSION_RATES:
        r_values = []  # 存储每个用户数量下的平均R-value
        for num_users in USER_COUNTS:
            total_r_value = 0
            for cycle in range(NUM_CYCLES):
                packets = generate_packets(num_users)

                # 使用贪心算法分配数据包
                allocation = allocate_packets(packets, NUM_SUBCARRIERS)

                # 计算该分配周期的R-value
                r_value = calculate_r_value(packets)

                # 累加总的R-value，便于计算平均值
                total_r_value += r_value

            # 计算并保存平均R-value
            avg_r_value = total_r_value / NUM_CYCLES
            r_values.append(avg_r_value)  # 保存每个用户数量下的平均R-value

            # 输出每个用户数量下的平均R-value
            print(f"用户数量: {num_users}, 平均R-value: {avg_r_value}")

        results[retransmission_rate] = r_values  # 保存结果
    return results
# 画图
def plot_results(results):
    for retransmission_rate, r_values in results.items():
        plt.plot(USER_COUNTS, r_values, label=f'Retransmission rate = {retransmission_rate}')
    plt.xlabel('Number of Users')
    plt.ylabel('Average R Value')
    plt.legend()
    plt.show()

# 运行仿真
results = run_simulation()
plot_results(results)
exit(0)