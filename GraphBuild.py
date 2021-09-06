import networkx as nx
import pandas as pd
import random
from tool import find_maxdegree_node
from operator import itemgetter


def build_network(graphtype,N):
    """
    创建/导入图数据
    :return: 图G
    """
    print('正在建立图……')
    if graphtype == 'ba':
        Graph = nx.barabasi_albert_graph(N, 5, seed=1)
    elif graphtype == 'ws':
        Graph = nx.watts_strogatz_graph(N, 10, 0.5)
    elif graphtype == 'dataset':
        Graph = nx.Graph()
        data = pd.read_csv('D:\\FYJ\\follower_followee.csv', encoding='gbk')
        print('正在导入图数据……', len(data))
        for i in range(0, len(data)):
            # print(i)
            followee_id = data[i:i + 1]['followee_id'].values
            followee_id = str(followee_id[0])
            follower_id = data[i:i + 1]['follower_id'].values
            follower_id = str(follower_id[0])
            if followee_id not in Graph.nodes:
                Graph.add_node(followee_id)
            if follower_id not in Graph.nodes:
                Graph.add_node(follower_id)
            Graph.add_edge(followee_id, follower_id)
    num_nodes = Graph.number_of_nodes()
    print('网络总节点数：', num_nodes)
    return Graph, num_nodes


def build_ego_network(N,m):
    Graph = nx.generators.barabasi_albert_graph(N, m, seed=1)
    node_and_degree = Graph.degree()
    (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    hub_ego = nx.ego_graph(Graph,largest_hub)
    num_nodes = hub_ego.number_of_nodes()
    print('ego网络总节点数：', num_nodes)
    return hub_ego, num_nodes


def initial_network(G, sa_num):
    """
    初始化图数据
    :param G: 输入图
    :param i_num: 感染者数量
    :param r_num: 免疫者数量
    """
    print('正在初始化图……')
    # 感染节点集
    max_node, max_de, sa_set = find_maxdegree_node(G)
    # i_set = set(G.nodes[max_node])
    # sa节点集
    # sa_set = set(random.sample(G.nodes, sa_num))
    # 两个集合不能重复
    # while max_node in sa_set:
    #     sa_set = set(random.sample(G.nodes, sa_num))

    # 初始化节点状态
    for node in G:
        G.nodes[node]['iftweet'] = False
        G.nodes[node]['ifread'] = False
        if node in sa_set:
            if node == max_node:
                G.nodes[node]['status'] = 'I'
                G.nodes[node]['Itime'] = 1
                G.nodes[node]['iftweet'] = True
                G.nodes[node]['ifread'] = True
            else:
                G.nodes[node]['status'] = 'Sa'
                G.nodes[node]['Satime'] = 1
                G.nodes[node]['readn'] = 0
        else:
            G.nodes[node]['status'] = 'Si'
            G.nodes[node]['readn'] = 0

    print('初始化完毕')
    return max_de