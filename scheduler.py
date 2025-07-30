import numpy as np

class Scheduler:
    """
    下行OFDMA资源单元调度器，支持不同的用户调度策略 (静态、轮询、最优)。
    """
    def __init__(self, num_users: int, strategy: str, snr_list: list = None):
        """
        初始化调度器。
        参数:
            num_users (int): 总用户数量。
            strategy (str): 调度策略，可为 "static"（静态）, "round-robin"（轮询）, "optimal"（最优）。
            snr_list (list): (可选) 每个用户的SNR(dB)列表，仅在optimal策略中使用。
        """
        self.num_users = num_users
        self.strategy = strategy.lower()
        # 并发RU的最大数量 (20MHz下最大支持9个26子载波RU)
        self.max_ru = 9
        # 轮询策略的当前指针
        self.rr_index = 0
        # 如果提供了snr_list，在optimal策略中使用
        self.snr_list = snr_list if snr_list is not None else [0] * num_users
        if self.strategy not in ["static", "round-robin", "optimal"]:
            raise ValueError(f"不支持的调度策略: {strategy}")
        # 如果是optimal策略，预先根据snr对用户排序的索引 (降序)
        if self.strategy == "optimal":
            # 记录每个用户的索引和对应snr
            indexed_snr = list(enumerate(self.snr_list))
            # 按snr值降序排序
            indexed_snr.sort(key=lambda x: x[1], reverse=True)
            # 提取排序后的用户索引列表
            self.sorted_users = [idx for idx, snr in indexed_snr]
        else:
            self.sorted_users = None

    def schedule(self, frame_idx: int):
        """
        为给定帧获取要调度的用户列表索引。
        参数:
            frame_idx (int): 当前帧序号（从0开始，可以用于某些调度策略）。
        返回:
            list: 本帧分配到RU的用户索引列表。
        """
        if self.strategy == "static":
            # 静态分配: 若用户数<=max_ru则全部用户每帧都调度；若用户数>max_ru则仅前max_ru个固定用户始终被调度，其余不调度
            active_users = list(range(min(self.num_users, self.max_ru)))
        elif self.strategy == "round-robin":
            # 轮询分配: 每帧依次为下一批用户分配RU
            active_users = []
            if self.num_users <= self.max_ru:
                # 用户数不超过RU数，全部用户同时调度
                active_count = self.num_users
            else:
                active_count = self.max_ru
            for i in range(active_count):
                idx = (self.rr_index + i) % self.num_users
                if idx not in active_users:
                    active_users.append(idx)
            # 更新轮询指针
            if self.num_users > 0:
                self.rr_index = (self.rr_index + active_count) % self.num_users
        elif self.strategy == "optimal":
            # 最优调度: 根据信道质量(SNR)选择snr最高的max_ru个用户
            if self.num_users <= self.max_ru:
                # 用户数不超过max_ru，全部调度
                active_users = list(range(self.num_users))
            else:
                # 选择snr最高的max_ru个用户
                active_users = self.sorted_users[:self.max_ru]
        else:
            active_users = []
        return active_users