import numpy as np
from modulation import QAMModem
from scheduler import Scheduler
from ofdma import OFDMA

def run_simulation(num_users: int, mcs: str, strategy: str, frames: int = 1000, snr: float = 20.0):
    """
    根据给定参数运行OFDMA仿真。
    参数:
        num_users (int): 用户数量。
        mcs (str): 调制方案 ("QPSK", "16QAM", "64QAM", "256QAM")。
        strategy (str): 资源单元分配策略 ("static", "round-robin", "optimal")。
        frames (int): 仿真的帧数 (次数)。
        snr (float): 信道平均SNR (以dB为单位)。
    返回:
        dict: 包含性能指标的字典，例如 {"throughput": ..., "BER": ..., "spectral_efficiency": ...}。
    """
    # 初始化调制解调器
    modem = QAMModem(mcs)
    # 为每个用户随机生成SNR值 (围绕给定均值snr上下浮动±5dB)，用于模拟不同用户信道质量
    # 若用户数为0，则直接返回空结果
    if num_users <= 0:
        return {"throughput": 0.0, "BER": 0.0, "spectral_efficiency": 0.0}
    # 设定随机SNR范围
    min_snr = max(0.0, snr - 5.0)
    max_snr = snr + 5.0
    snr_list = list(np.random.uniform(min_snr, max_snr, size=num_users))
    # 初始化调度器和OFDMA模拟器
    scheduler = Scheduler(num_users, strategy, snr_list=snr_list)
    ofdma_sim = OFDMA(total_subcarriers=234, modem=modem, snr_list=snr_list)
    total_bits = 0
    total_errors = 0
    # 仿真指定帧次数
    for frame in range(frames):
        # 获取本帧调度的用户
        active_users = scheduler.schedule(frame)
        # 传输本帧并获取传输的比特数和错误数
        bits, errors = ofdma_sim.transmit_frame(active_users)
        total_bits += bits
        total_errors += errors
    # 计算性能指标
    if total_bits == 0:
        ber = 0.0
        throughput_bps = 0.0
    else:
        ber = total_errors / total_bits
        # 计算吞吐量 (比特/秒)，假设每帧对应1ms传输时间
        total_time_s = frames * 1e-3  # 1ms per frame
        # 计算正确接收的比特数
        bits_delivered = total_bits - total_errors
        throughput_bps = bits_delivered / total_time_s
    # 频谱利用率 = 吞吐量(比特/秒) / 带宽(Hz)
    bandwidth_hz = 20e6  # 20 MHz
    spectral_efficiency = throughput_bps / bandwidth_hz if bandwidth_hz > 0 else 0.0
    results = {
        "throughput": throughput_bps,
        "BER": ber,
        "spectral_efficiency": spectral_efficiency
    }
    return results