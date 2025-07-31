import numpy as np

class OFDMA:
    """
    简化的802.11ax OFDMA下行链路模拟类。负责将比特映射到资源单元并通过信道传输。
    """
    def __init__(self, total_subcarriers: int, modem, snr_list: list):
        """
        初始化OFDMA模拟器。
        参数:
            total_subcarriers (int): 总子载波数量（20MHz信道，默认234个数据子载波）。
            modem: QAMModem调制解调对象（用于所有用户的调制解调）。
            snr_list (list): 每个用户的SNR(dB)列表。
        """
        self.total_subcarriers = total_subcarriers
        self.modem = modem
        self.snr_list = snr_list

    def transmit_frame(self, active_users: list):
        """
        模拟一次OFDMA帧传输（一次下行多用户发送）。
        参数:
            active_users (list): 本帧获得资源单元的用户索引列表。
        返回:
            tuple: (bits_transmitted, bit_errors) 此帧传输了多少比特，发生了多少比特错误。
        """
        bits_transmitted = 0
        bit_errors = 0
        num_active = len(active_users)
        if num_active == 0:
            return 0, 0
        # 每个用户分配的子载波数（取整）
        subc_per_user = self.total_subcarriers // num_active
        # 针对每个活动用户生成随机数据、进行调制、通过信道并解调
        for user in active_users:
            # 计算本用户本帧可用的比特数量 = 子载波数 * 每子载波可承载比特数
            bits_per_symbol = self.modem.bits_per_symbol
            user_bits_count = subc_per_user * bits_per_symbol
            if user_bits_count == 0:
                continue  # 若子载波为0则跳过
            # 生成随机比特
            tx_bits = np.random.randint(0, 2, user_bits_count)
            # 调制得到发送符号
            tx_symbols = self.modem.modulate(tx_bits)
            # 获取该用户SNR并计算噪声标准差
            snr_db = self.snr_list[user]
            snr_linear = 10 ** (snr_db / 10.0)
            noise_sigma = np.sqrt(1 / (2 * snr_linear))
            # 生成AWGN噪声
            noise = noise_sigma * (np.random.randn(len(tx_symbols)) + 1j * np.random.randn(len(tx_symbols)))
            # 通过信道（加性噪声，假设理想信道增益为1）
            rx_symbols = tx_symbols + noise
            # 接收端解调
            rx_bits = self.modem.demodulate(rx_symbols)
            # 统计比特错误
            errors = np.sum(tx_bits != rx_bits)
            bits_transmitted += user_bits_count
            bit_errors += errors
        return bits_transmitted, bit_errors