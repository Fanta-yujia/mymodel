import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tool import count_nodenum
from model import update_network
from GraphBuild import build_network, initial_network


def save_gragh():
    # 总人数
    N = 10000

    # 感染者人数
    i = 1
    # 活跃者人数
    sa = 20000

    G1, num_nodes = build_network('dataset',20000)
    # G2, num_nodes = build_network('dataset',20000)
    # initial_network(G2, sa)
    # G3, num_nodes = build_network('dataset',20000)
    # initial_network(G3, sa)
    nx.write_gexf(G1, 'dataset_G1.gexf')
    print('g1写入完毕')
    nx.write_gexf(G1, 'dataset_G2.gexf')
    print('g2写入完毕')
    nx.write_gexf(G1, 'dataset_G3.gexf')
    print('g3写入完毕')


if __name__ == '__main__':
    save_gragh()
    g1 = nx.read_gexf("dataset_G1.gexf")
    print('g1读取完毕')
    g2 = nx.read_gexf("dataset_G2.gexf")
    print('g2读取完毕')
    g3 = nx.read_gexf("dataset_G3.gexf")
    print('g3读取完毕')


