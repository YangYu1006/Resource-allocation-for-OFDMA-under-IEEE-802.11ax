import argparse
from simulator import run_simulation

def main():
    parser = argparse.ArgumentParser(
        description="IEEE 802.11ax OFDMA仿真器 - 模拟下行OFDMA性能"
    )
    parser.add_argument(
        "-u", "--users", type=int, required=True, help="STA用户数量"
    )
    parser.add_argument(
        "-m", "--mcs", type=str, choices=["QPSK", "16QAM", "64QAM", "256QAM","1024QAM"], required=True,
        help="调制方式 (QPSK, 16QAM, 64QAM, 256QAM, 1024QAM)"
    )
    parser.add_argument(
        "-s", "--strategy", type=str, choices=["static", "round-robin", "optimal"], required=True,
        help="资源单元分配策略 (static 静态, round-robin 轮询, optimal 最优)"
    )
    parser.add_argument(
        "-f", "--frames", type=int, default=1000, help="模拟帧数 (默认: 1000)"
    )
    parser.add_argument(
        "--snr", type=float, default=20.0, help="平均信噪比SNR(dB) (默认: 20.0)"
    )
    args = parser.parse_args()
    # 运行仿真
    results = run_simulation(num_users=args.users, mcs=args.mcs, strategy=args.strategy,
                             frames=args.frames, snr=args.snr)
    # 提取结果
    throughput = results["throughput"]
    ber = results["BER"]
    spec_eff = results["spectral_efficiency"]
    # 以易读格式打印结果
    # 将吞吐量转换为 Mbps
    throughput_mbps = throughput / 1e6
    print(f"用户数: {args.users}")
    print(f"调制方式: {args.mcs}")
    print(f"调度策略: {args.strategy}")
    print(f"帧数: {args.frames}")
    print(f"SNR: {args.snr:.1f} dB")
    print("---- 仿真结果 ----")
    print(f"吞吐量: {throughput_mbps:.2f} Mbps")
    print(f"误码率 (BER): {ber:.2e}")
    print(f"频谱利用率: {spec_eff:.2f} bit/s/Hz")

if __name__ == "__main__":
    main()