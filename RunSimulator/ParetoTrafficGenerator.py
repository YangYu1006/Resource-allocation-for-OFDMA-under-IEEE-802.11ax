import numpy as np
import simpy


from ns.packet.dist_generator import DistPacketGenerator
from ns.packet.sink import PacketSink
from ns.port.port import Port

i = 0
PacketSize = []
while (i<11):
    def packet_arrival():
        return 1.5
    packetsize = np.random.pareto(a=1,size=1)*10000
    def packet_size():
        return packetsize
    PacketSize.append(packet_size())
    env = simpy.Environment()
    ps = PacketSink(env, debug=True)
    pg = DistPacketGenerator(env, "pg", packet_arrival, packet_size, flow_id=0)
    port = Port(env, rate=200.0, qlimit=300)

    pg.out = port
    port.out = ps

    env.run(until=20)
    print('%2f,'%packetsize,end="")
    i = i+1
exit(0)