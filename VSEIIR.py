import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
# 确保 中文 和 -
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def update_node_status(G, node, p1, p2, p3, v2):
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
                    break
    # 如果当前节点状态为 阅读者(E) 有概率p2变为 感染者(I)
    elif G.nodes[node]['status'] == 'E':
        # for adj_node in G[node]:
        #     if G.nodes[adj_node]['status'] == 'I':
        p = random.random()
        if p < p2:
            G.nodes[node]['status'] = 'I'
            G.nodes[node]['Itime'] = 1
            # break
        if G.nodes[node]['status'] == 'E':
            G.nodes[node]['Etime'] -= v2
            if G.nodes[node]['Etime'] <= 0:
                G.nodes[node]['status'] = 'R'


def update_network(G, paras, i_num):
    """
    更新图的每个节点状态
    :param G: 图
    :param paras: 各个参数
    :param i_num: I节点数
    :return:
    """
    print('updating……')
    hot = i_num / G.number_of_nodes()
    c, l, r, fi, fa, v1, v2 = paras
    p1 = c ** (np.log10(l + 1))
    p2 = (0.3* hot + 0.3 * r) ** (np.log10(1 / fi))
    p3 = (hot + r) ** (np.log10(1 / fa))
    for node in G:
        # 如果当前节点状态为 感染者(I) 以v1的速率变为 免疫者(R)
        if G.nodes[node]['status'] == 'I':
            G.nodes[node]['Itime'] -= v1
            if G.nodes[node]['Itime'] <= 0:
                G.nodes[node]['status'] = 'R'
    for node in G:
        update_node_status(G, node, p1, p2, p3, v2)


def count_nodenum(G):
    """
    计算当前图内各个节点的数目
    :param G: 输入图
    :return: 各个状态的节点数目
    """
    si_num, e_num, i_num, r_num, sa_num = 0, 0, 0, 0, 0
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
    return si_num, e_num, i_num, r_num, sa_num


def build_network(type):
    """
    创建/导入图数据
    :return: 图G
    """
    print('正在建立图……')
    if type == 'ba':
        Graph = nx.barabasi_albert_graph(N, 3, seed=1)
    elif type == 'ws':
        Graph = nx.watts_strogatz_graph(N, 10, 0.5)
    elif type == 'dataset':
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
    return Graph


def initial_network(G, i_num, sa_num):
    """
    初始化图数据
    :param G: 输入图
    :param i_num: 感染者数量
    :param r_num: 免疫者数量
    """
    print('正在初始化图……')
    # 感染节点集
    i_set = set(random.sample(G.nodes, i_num))
    # sa节点集
    sa_set = set(random.sample(G.nodes, sa_num))
    # 两个集合不能重复
    while sa_set & i_set:
        sa_set = set(random.sample(G.nodes, sa_num))
    # 初始化节点状态
    for node in G:
        if node in i_set:
            G.nodes[node]['status'] = 'I'
            G.nodes[node]['Itime'] = 1
        elif node in sa_set:
            G.nodes[node]['status'] = 'Sa'
        else:
            G.nodes[node]['status'] = 'Si'
    print('初始化完毕')


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


def draw_node_trend(G, paras):
    """
    输出各类节点趋势
    :param G: 输入图
    :param beta: 感染率
    """
    # 设定传播步长
    t_list = np.linspace(1,50)
    # 开始模拟传播
    for t in range(len(t_list)):
        # 计算并存储当前各个节点数目
        nums = count_nodenum(G)
        print(t, ': ', nums)
        node_list.append(nums)
        update_network(G, paras, nums[2])
    # 整理数据
    df = pd.DataFrame(data=node_list, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa'])
    # 显示数据曲线
    df.plot(figsize=(8, 6), color=[color_dict.get(x) for x in df.columns])
    plt.ylabel('nodes')
    plt.xlabel('days')
    plt.title('VSEIIR_model')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    plt.savefig('VSEIIR_model')
    plt.show()


def draw_param_compare(G, paras1,paras2):
    """
    输出参数对此实验
    :param G: 输入图
    :param beta: 感染率
    """
    G1=G
    G2=G
    # 设定传播步长
    t_list = np.linspace(1,50)
    # 开始模拟传播
    for t in range(len(t_list)):
        # 计算并存储当前各个节点数目
        nums = count_nodenum(G1)
        print(t, ': ', nums)
        node_list.append(nums)
        update_network(G1, paras1, nums[2])
    # 整理数据
    df = pd.DataFrame(data=node_list, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa'])
    # 显示数据曲线
    df.plot(figsize=(8, 6), color=[color_dict.get(x) for x in df.columns])
    plt.ylabel('nodes')
    plt.xlabel('days')
    plt.title('VSEIIR_model')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    plt.savefig('VSEIIR_model')
    plt.show()


def update_graph(i, G, ax, pos, paras):
    """
    动态更新节点
    :param i: 输入帧
    :param ax: 输入图参数
    :param G: 输入图
    :param beta: 感染率
    :param gamma: 免疫率
    """
    i = int(i)
    print(i)
    ax.set_title("第" + str(i + 1) + "天 节点分布")
    ax.axis('off')
    plt.box(False)
    if i == 1:
        # 第一天  初始节点分布  直接画出
        nx.draw(G, with_labels=True, font_color='white', edge_color='grey',
                node_color=[color_dict[G.nodes[node]['status']] for node in G], pos=pos)
    else:
        # 以后变化 需要演变节点
        update_network(G, paras, count_nodenum(G)[2])
        nx.draw_networkx_nodes(G, with_labels=True, font_color='white', edge_color='grey',
                               node_color=[color_dict[G.nodes[node]['status']] for node in G], pos=pos)


def draw_graph_change(G, days):
    """
    输出网络动态变化视频
    :param G: 输入图
    :param beta: 感染率
    :param gamma: 免疫率
    :param days: 需要的时间(迭代次数)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G, scale=1)
    ani = animation.FuncAnimation(fig, update_graph, frames=days,
                                   interval=300,blit=True)
    writer = animation.FFMpegWriter()
    ani.save('./network_trend.mp4', writer=writer)


if __name__ == '__main__':
    # 总人数
    N = 10000

    # 感染者人数
    i = 1
    # 活跃者人数
    sa = 10000
    # 非活跃者人数
    si = N - i - sa
    # c, l, r, fi, fa, v1, v2 = paras
    paras = [5, 4, 0.6, 1/10, 1/2, 0.2, 0.4]
    # 各个节点数目列表
    node_list = []

    # 节点颜色
    color_dict = {'Si': 'blue', 'E': 'yellow', 'I': 'red', 'R': 'green', 'Sa': 'black'}
    # 创建网络
    G = build_network('dataset')
    # 初始化网络节点
    initial_network(G, i, sa)
    # 第一天  初始节点分布  直接画出

    # 输出节点趋势图
    draw_node_trend(G, paras)
    # 初始节点分布图
    # 输出初始节点网络图
    # draw_network(G)
    # 输出网络动态变化图
    # draw_graph_change(G, 10)