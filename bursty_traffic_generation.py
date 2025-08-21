import simpy
import numpy as np
from functools import partial
from random import randint, seed

from ns.packet.dist_generator import DistPacketGenerator
from ns.packet.sink import PacketSink
from ns.utils.generators.MAP_MSP_generator import BMAP_generator

MIN_PKT_SIZE = 100
MAX_PKT_SIZE = 1000

def packet_size(myseed=None):
    seed(myseed)
    return randint(MIN_PKT_SIZE, MAX_PKT_SIZE)

def interarrival(y):
    try:
        return next(y)
    except StopIteration:
        return

def generate_flow_packet_sizes(simulation_time=20, pg_duration=18):
    env = simpy.Environment()
    ps = PacketSink(env)

    D0 = np.array([[-114.46031, 11.3081, 8.42701],
                   [158.689, -29152.1587, 20.5697],
                   [1.08335, 0.188837, -1.94212]])
    D1 = np.array([[94.7252, 0.0, 0.0],
                   [0.0, 2.89729e4, 0.0],
                   [0.0, 0.0, 0.669933]])
    y = BMAP_generator([D0, D1])

    iat_dist = partial(interarrival, y)
    pkt_size_dist = partial(packet_size)

    pg = DistPacketGenerator(env,
                             'flow_1',
                             iat_dist,
                             pkt_size_dist,
                             flow_id='flow_1',
                             initial_delay=0.0,
                             finish=pg_duration)
    pg.out = ps

    env.run(until=simulation_time)
    return ps.packet_sizes['flow_1']  # 返回列表