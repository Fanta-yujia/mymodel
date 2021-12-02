import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from tool import get_p1
# 确保 中文 和 -
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def update_node_status(G, node, p1, p2, p3, v2,v3):
    """
    更改节点状态
    :param G: 图
    :param node: 节点
    :param p1: 阅读率
    :param p2: 非活跃转发率
    :param p3: 活跃转发率
    :param v2: E的免疫速率
    :return:
    """
    # 如果当前节点状态为 非活跃者(Si) 有概率p1变为 阅读者(E)
    if G.nodes[node]['status'] == 'Si':
        for adj_node in G[node]:
            if G.nodes[adj_node]['status'] == 'I' and G.nodes[adj_node]['Itime'] != 1:
                p = random.random()
                if p < p1:
                    G.nodes[node]['status'] = 'E'
                    G.nodes[node]['Etime'] = 1
                    break
    # 如果当前节点状态为 活跃者(Sa) 有概率p3变为 感染者(I)
    elif G.nodes[node]['status'] == 'Sa':
        for adj_node in G[node]:
            if G.nodes[adj_node]['status'] == 'I' and G.nodes[adj_node]['Itime'] != 1:
                p = random.random()
                if p < p3:
                    G.nodes[node]['status'] = 'I'
                    G.nodes[node]['Itime'] = 1
                    G.nodes[node]['iftweet'] = True
                    break
        if G.nodes[node]['status'] == 'Sa':
            G.nodes[node]['Satime'] -= v3
            if G.nodes[node]['Satime'] <= 0:
                G.nodes[node]['status'] = 'R'
    # 如果当前节点状态为 阅读者(E) 有概率p2变为 感染者(I)
    elif G.nodes[node]['status'] == 'E':
        # for adj_node in G[node]:
        #     if G.nodes[adj_node]['status'] == 'I':
        p = random.random()
        if p < p2:
            G.nodes[node]['status'] = 'I'
            G.nodes[node]['Itime'] = 1
            G.nodes[node]['iftweet'] = True
            # break
        else:
            G.nodes[node]['Etime'] -= v2
            if G.nodes[node]['Etime'] <= 0:
                G.nodes[node]['status'] = 'R'


def update_network(G, paras, tweet_num):
    """
    更新图的每个节点状态
    :param G: 图
    :param paras: 各个参数
    :param i_num: I节点数
    :return:
    """
    # print('updating……')
    hot = tweet_num / G.number_of_nodes()
    on, r, fi, fa, v1, v2, v3 = paras
    p1 = on
    p2 = (0.5 * hot + 0.5 * r) ** (np.log10(1 / fi))
    p3 = (hot + r) ** (np.log10(1 / fa))
    for node in G:
        # 如果当前节点状态为 感染者(I) 以v1的速率变为 免疫者(R)
        if G.nodes[node]['status'] == 'I':
            G.nodes[node]['Itime'] -= v1
            if G.nodes[node]['Itime'] <= 0:
                G.nodes[node]['status'] = 'R'
    for node in G:
        update_node_status(G, node, p1, p2, p3, v2,v3)


def new_model(G, paras, hot, t):
    # hot = tweet_num / G.number_of_nodes()
    pubtime, r, fi, fa, v1, v2, v3 = paras
    p1 = get_p1(pubtime, t)
    # p2 = (0.7 * hot + 0.3 * r) ** (np.log10(1 / fi))
    # p3 = (0.3 * hot + 0.7 * r) ** (np.log10(1 / fa))
    p3 = 0.3 * hot + 0.7 * r
    for node in G:
        # 如果当前节点状态为 感染者(I) ,向每个邻居发消息
        if G.nodes[node]['status'] == 'I':
            I_de = G.degree(node)
            # p2 = (0.5 * hot + 0.2 * r + 0.3*I_de/max_de) ** (np.log10(1 / fi))
            # p2 = 0.4 * hot + 0.3 * r + 0.3 * I_de / max_de
            p2 = 0.8 * hot + 0.3 * r
            for adj_node in G[node]:
                if G.nodes[adj_node]['status'] == 'Si':
                    p = random.random()
                    if p < p1:
                        G.nodes[adj_node]['status'] = 'E'
                        G.nodes[adj_node]['Etime'] = 1
                        G.nodes[adj_node]['readn'] += 1
                        G.nodes[adj_node]['ifread'] = True
                elif G.nodes[adj_node]['status'] == 'E':
                    G.nodes[adj_node]['readn'] += 1
                    x = G.nodes[adj_node]['readn']
                    p2_new = p2*(1/1)*x*np.exp(1-x/1)
                    p = random.random()
                    if p < p2_new:
                        G.nodes[adj_node]['status'] = 'I'
                        G.nodes[adj_node]['Itime'] = 1
                        G.nodes[adj_node]['iftweet'] = True
                elif G.nodes[adj_node]['status'] == 'Sa':
                    G.nodes[adj_node]['ifread'] = True
                    G.nodes[adj_node]['readn'] += 1
                    x = G.nodes[adj_node]['readn']
                    p3_new = p3
                    p = random.random()
                    if p < p3_new:
                        G.nodes[adj_node]['status'] = 'I'
                        G.nodes[adj_node]['Itime'] = 1
                        G.nodes[adj_node]['iftweet'] = True
            G.nodes[node]['Itime'] -= v1
            if G.nodes[node]['Itime'] <= 0:
                G.nodes[node]['status'] = 'R'
        elif G.nodes[node]['status'] == 'E':
            G.nodes[node]['Etime'] -= v2
            if G.nodes[node]['Etime'] <= 0:
                G.nodes[node]['status'] = 'R'
        elif G.nodes[node]['status'] == 'Sa':
            if G.nodes[node]['readn'] != 0:
                G.nodes[node]['Satime'] -= v3
                if G.nodes[node]['Satime'] <= 0:
                    G.nodes[node]['status'] = 'R'

def SEIIR_model(G):
    c=0.06
    l=4
    r=0.5
    p1 = c ** (np.log10(l+1))
    p1=0.7
    p2 = (1-r) ** (np.log10(l+1))
    p2 = 0.5
    v1 =0.2
    v2 = 0.2
    v3 = 0.05
    p3 = r
    for node in G:
        # 如果当前节点状态为 感染者(I) ,向每个邻居发消息
        if G.nodes[node]['status'] == 'I':
            for adj_node in G[node]:
                if G.nodes[adj_node]['status'] == 'Si':
                    p = random.random()
                    if p < p1:
                        G.nodes[adj_node]['status'] = 'E'
                        G.nodes[adj_node]['Etime'] = 1
                elif G.nodes[adj_node]['status'] == 'Sa':
                    p = random.random()
                    if p < p3:
                        G.nodes[adj_node]['status'] = 'I'
                        G.nodes[adj_node]['Itime'] = 1
                        G.nodes[adj_node]['iftweet'] = True
            p = random.random()
            if p < p2:
                G.nodes[node]['status'] = 'R'
            else:
                G.nodes[node]['Itime'] -= v3
                if G.nodes[node]['Itime'] <= 0:
                    G.nodes[node]['status'] = 'R'
        elif G.nodes[node]['status'] == 'E':
            p = random.random()
            if p < v1:
                G.nodes[node]['status'] = 'I'
                G.nodes[node]['Itime'] = 1
                G.nodes[node]['iftweet'] = True
            else:
                p = random.random()
                if p < v2:
                    G.nodes[node]['status'] = 'R'
                # G.nodes[node]['Etime'] -= v2
                # if G.nodes[node]['Etime'] <= 0:
                #     G.nodes[node]['status'] = 'R'





