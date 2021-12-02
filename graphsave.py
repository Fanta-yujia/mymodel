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

    # G1, num_nodes = build_network('dataset',20000)
    G2, num_nodes2 = build_network('ba', 99000)
    nx.write_gexf(G2, 'dataset_G2.gexf')
    print('g2写入完毕')
    G3, num_nodes3 = build_network('ws', 99000)
    nx.write_gexf(G3, 'dataset_G3.gexf')
    print('g3写入完毕')

def draw_network(G):
    """
    输出初始网络节点分布
    :param G: 输入图
    """
    # 设置图大小
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title("节点初始分布")
    pos = nx.spring_layout(G, scale=1)
    nx.draw(G, pos=pos, with_labels=True, font_color='white', edge_color='grey',
            node_color=[color_dict[G.nodes[node]['status']] for node in G])



if __name__ == '__main__':
    # save_gragh()
    # g1 = nx.read_gexf("dataset_G1.gexf")
    # print('g1读取完毕')
    # g1ac=nx.average_shortest_path_length(g1)
    # g1ap=nx.average_clustering(g1)
    # print('weibo平均聚类系数', g1ac)
    # print('weibo平均最短路径',g1ap)

    g2 = nx.read_gexf("dataset_G2.gexf")
    # degree=nx.degree_histogram(g3)
    # x=range(len(degree))
    # y=[z/float(sum(degree))for z in degree]


    # plt.scatter(x,y,s=4,c='red')
    # plt.show()
    print('g2读取完毕')
    print(nx.diameter(g2))

    # g2ac=nx.average_shortest_path_length(g2)
    # print(dict(nx.all_pairs_shortest_path(g2)))
    # print('BA平均最短路径', g2ac)
    # # assert_almost_equal(g2ac, 2)
    # print('average diameter: {}'.format(nx.diameter(g2)))

    # g2ap=nx.average_clustering(g2)
    # print('BA平均最短路径',g2ap)
    #
    # g3 = nx.read_gexf("dataset_G3.gexf")
    # print('g3读取完毕')
    # g3ac=nx.average_shortest_path_length(g3)
    # g3ap=nx.average_clustering(g3)
    # print('WS平均聚类系数', g3ac)
    # print('WS平均最短路径',g3ap)


