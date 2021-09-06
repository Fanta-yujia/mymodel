import networkx as nx
import random
from operator import itemgetter


def count_nodenum(G):
    """
    计算当前图内各个节点的数目
    :param G: 输入图
    :return: 各个状态的节点数目
    """
    si_num, e_num, i_num, r_num, sa_num = 0, 0, 0, 0, 0
    tweet_num = 0
    read_num = 0
    for node in G:
        if G.nodes[node]['status'] == 'Sa':
            sa_num += 1
        elif G.nodes[node]['status'] == 'Si':
            si_num += 1
        elif G.nodes[node]['status'] == 'E':
            e_num += 1
        elif G.nodes[node]['status'] == 'I':
            i_num += 1
        else:
            r_num += 1
        if G.nodes[node]['iftweet']:
            tweet_num += 1
        if G.nodes[node]['ifread']:
            read_num += 1

    return si_num, e_num, i_num, r_num, sa_num, tweet_num,read_num


def find_maxdegree_node(Graph):
    # max_de = 0
    # for node in G:
    #     de = G.degree(node)
    #     if de > max_de:
    #         max_de = de
    #         max_node = node
    node_and_degree = Graph.degree()
    sortedlist = sorted(node_and_degree, key=itemgetter(1))
    (max_node, max_de) = sortedlist[-1]
    print('度最大的节点', str(max_node), str(max_de))
    sa_list=[]
    print('其他度大的节点：')
    for t in sortedlist[-2000:]:
        print(t[0],t[1])
        sa_list.append(t[0])
    return max_node, max_de, sa_list


def get_p1(ptime, t):
    time = (ptime+t) % 24
    print(f'当前时间：{str(time)}点！', end="")
    if 0 <= time < 8:
        p = 0.1
    elif 8 <= time < 11 or 14 <= time < 18:
        p = 0.3
    elif 11 <= time < 14:
        p = 0.7
    else:
        p = 0.8
    print(f'只有{p}的用户上线率')
    return p



