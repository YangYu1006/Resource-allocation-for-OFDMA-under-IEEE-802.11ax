import numpy as np

class QAMModem:
    """
    QAM调制解调器类，支持 QPSK、16QAM、64QAM、256QAM、1024QAM 的调制和解调。
    """
    def __init__(self, scheme: str):
        """
        初始化调制解调器。
        参数:
            scheme (str): 调制方式名称，例如 "QPSK", "16QAM", "64QAM", "256QAM","1024QAM"。
        """
        scheme = scheme.upper()
        self.scheme = scheme
        # 根据调制方案设置每符号比特数
        if scheme == "QPSK":
            self.bits_per_symbol = 2
        elif scheme == "16QAM":
            self.bits_per_symbol = 4
        elif scheme == "64QAM":
            self.bits_per_symbol = 6
        elif scheme == "256QAM":
            self.bits_per_symbol = 8
        elif scheme == "1024QAM":
            self.bits_per_symbol = 10
        else:
            raise ValueError(f"不支持的调制方式: {scheme}")
        # 调制阶数 M
        self.M = 2 ** self.bits_per_symbol
        # 每个轴上的星座点数量 (I和Q轴各自的点数)
        self.sqrtM = 2 ** (self.bits_per_symbol // 2)
        # 生成星座图各电平的取值列表 (PAM序列)，例如对于16QAM，levels = [-3, -1, 1, 3]
        k = self.sqrtM
        # 生成等间隔的奇数值序列，从 -(k-1) 到 (k-1)，步长为2
        self.levels = np.array([-(k - 1) + 2 * i for i in range(k)])
        # 归一化星座图能量，使平均能量为1
        average_power = np.mean(np.abs(self.levels) ** 2)
        self.levels = self.levels / np.sqrt(average_power)

    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        将比特序列进行调制，生成复数星座点序列。
        参数:
            bits (np.ndarray): 0/1比特数组 (一维)。
        返回:
            np.ndarray: 调制后的复数符号数组。
        """
        if len(bits) % self.bits_per_symbol != 0:
            bits = bits[: len(bits) - (len(bits) % self.bits_per_symbol)]
        bps = self.bits_per_symbol
        half = bps // 2
        bit_groups = bits.reshape(-1, bps)
        I_bits = bit_groups[:, :half]
        Q_bits = bit_groups[:, half:]
        weights = 2 ** np.arange(half - 1, -1, -1)
        I_indices = I_bits.dot(weights)
        Q_indices = Q_bits.dot(weights)
        I_symbols = self.levels[I_indices]
        Q_symbols = self.levels[Q_indices]
        symbols = I_symbols + 1j * Q_symbols
        return symbols

    def demodulate(self, symbols: np.ndarray) -> np.ndarray:
        """
        将接收到的复数符号序列解调为比特序列。
        参数:
            symbols (np.ndarray): 接收的复数符号数组。
        返回:
            np.ndarray: 解调得到的0/1比特数组。
        """
        I_vals = np.real(symbols)
        Q_vals = np.imag(symbols)
        I_diffs = np.abs(I_vals[:, None] - self.levels[None, :])
        I_indices = I_diffs.argmin(axis=1)
        Q_diffs = np.abs(Q_vals[:, None] - self.levels[None, :])
        Q_indices = Q_diffs.argmin(axis=1)
        half = self.bits_per_symbol // 2
        num_symbols = len(symbols)
        bits_out = np.zeros(num_symbols * self.bits_per_symbol, dtype=int)
        for i in range(num_symbols):
            I_idx = I_indices[i]
            Q_idx = Q_indices[i]
            # I轴比特
            for b in range(half):
                bits_out[i * self.bits_per_symbol + b] = (I_idx >> (half - 1 - b)) & 1
            # Q轴比特
            for b in range(half):
                bits_out[i * self.bits_per_symbol + half + b] = (Q_idx >> (half - 1 - b)) & 1
        return bits_out