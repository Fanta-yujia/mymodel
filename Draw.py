import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tool import count_nodenum
from model import update_network,new_model
from GraphBuild import build_network, initial_network,build_ego_network
# 确保 中文 和 -
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def start_diffusion(G, paras, t_list, max_de):
    """
    输出各类节点趋势
    :param G: 输入图
    :param beta: 感染率
    """
    node_list = []
    # 开始模拟传播
    for t in range(len(t_list)):
        # 计算并存储当前各个节点数目
        nums = count_nodenum(G)
        nums = [num / num_nodes for num in nums]
        print(t, ': ', nums)
        node_list.append(nums)
        new_model(G, paras, nums[-2], t, max_de)
    return node_list

def draw_node_trend(node_list):
    """
    输出各类节点趋势
    :param G: 输入图
    :param beta: 感染率
    """
    # 整理数据
    df = pd.DataFrame(data=node_list, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    # 显示数据曲线
    df1 = df[['Si', 'E', 'I', 'R', 'Sa','tweet']]
    df1.plot(figsize=(8, 6), color=[color_dict.get(x) for x in df1.columns])
    plt.ylabel('percent')
    plt.xlabel('time/h')
    plt.title('VSEIIR_model')
    plt.savefig('09022238_all nodes')
    plt.show()

    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    # plt.savefig('08262156_VSEIIR_model')
    # df2 = df[['tweet', 'read']]
    # # 显示数据曲线
    # df2.plot(figsize=(8, 6), color=[color_dict.get(x) for x in df2.columns])
    # plt.ylabel('percent')
    # plt.xlabel('time/h')
    # plt.title('tweet and read percents')
    # plt.show()
    # plt.savefig('09022045_tweet and read')



def draw_tweet_change(node_list):
    # 显示数据曲线
    df = pd.DataFrame(data=node_list, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df = df['tweet']
    df.plot(figsize=(8, 6), color='orange')
    plt.ylabel('tweets')
    plt.xlabel('days')
    plt.title('tweet_change of VSEIIR_model')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    plt.savefig('tweet_change of VSEIIR_model')
    plt.show()


def draw_param_compare():
    """
    输出参数对此实验
    :param G: 输入图
    :param beta: 感染率
    """
    t_list = np.linspace(1, 50)
    # 设定传播步长
    node_list_1 = start_diffusion(G1, paras1, t_list)
    df1 = pd.DataFrame(data=node_list_1, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df1 = df1['tweet']
    node_list_2 = start_diffusion(G2, paras2, t_list)
    df2 = pd.DataFrame(data=node_list_2, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df2 = df2['tweet']
    node_list_3 = start_diffusion(G3, paras3, t_list)
    df3 = pd.DataFrame(data=node_list_3, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df3 = df3['tweet']
    node_list_4 = start_diffusion(G4, paras4, t_list)
    df4 = pd.DataFrame(data=node_list_4, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df4 = df4['tweet']
    # 显示数据曲线
    df1.plot(color='gold',style='.-')
    df2.plot(color='orange', style='o-')
    df3.plot(color='orangered', style='*-')
    df4.plot(color='darkred', style='s-')
    plt.ylabel('tweet_nodes_percent')
    plt.xlabel('time/h')
    plt.legend(['v1=0.1', 'v1=0.3', 'v1=0.5', 'v1=0.7'], loc='lower right')
    plt.title('不同感染者免疫速率下的转发比例变化对比')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    plt.savefig('v1_VSEIIR_dataset')
    plt.show()


def draw_network_compare(paras):
    """
    输出参数对此实验
    :param G: 输入图
    :param beta: 感染率
    """
    G1 = nx.read_gexf("dataset_G1.gexf")
    print('g1读取完毕')
    G2 = nx.read_gexf("dataset_G2.gexf")
    print('g2读取完毕')
    # 设定传播步长
    t_list = np.linspace(1, 50)

    node_list_1 = start_diffusion(G1, paras, t_list)
    df1 = pd.DataFrame(data=node_list_1, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df1 = df1['I']
    node_list_2 = start_diffusion(G2, paras, t_list)
    df2 = pd.DataFrame(data=node_list_2, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df2 = df2['I']
    # 显示数据曲线
    df1.plot(color='orange', style='-')
    df2.plot(color='orangered', style='--')
    plt.ylabel('nodes_number')
    plt.xlabel('days')
    plt.legend(['BA无标度网络', 'WS小世界网络'], loc='lower right')
    plt.title('ba_ws_VSEIIR_model')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    plt.savefig('ba_ws_VSEIIR_model_dataset')
    plt.show()



if __name__ == '__main__':
    N = 10000  # 总人数
    i = 1  # 感染者人数
    sa_num = 10000  # 活跃者人数

    # 非活跃者人数
    # si = N - i - sa
    # 参数 [pubtime, r, fi, fa, v1, v2, v3]
    paras = [5, 0.8, 1/8, 1/2, 0.05, 0.2, 0.1]
    # 各个节点数目列表

    # 节点颜色
    color_dict = {'Si': 'blue', 'E': 'yellow', 'I': 'red', 'R': 'black', 'Sa': 'green',
                  'tweet': 'orange', 'read': 'darkred'}
    # 创建网络
    #G, num_nodes = build_network('dataset',20000)
    G = nx.read_gexf("dataset_G1.gexf")
    # G, num_nodes = build_ego_network(100000,5)

    # 初始化网络节点
    max_de = initial_network(G, sa_num)
    num_nodes = G.number_of_nodes()
    # 开始传播
    t_list = np.linspace(1, 50)
    node_list = start_diffusion(G, paras, t_list, max_de)
    # 输出节点趋势图
    draw_node_trend(node_list)
    # # draw_tweet_change(node_list)


    # paras1 = [0.5, 0.6, 1/8, 1/2, 0.1, 0.3, 0.3]
    # paras2 = [0.5, 0.6, 1/8, 1/2, 0.3, 0.3, 0.3]
    # paras3 = [0.5, 0.6, 1/8, 1/2, 0.5, 0.3, 0.3]
    # paras4 = [0.5, 0.6, 1/8, 1/2, 0.7, 0.3, 0.3]
    # G1 = nx.read_gexf("dataset_G1.gexf")
    # print('g1读取完毕')
    # initial_network(G1, sa)
    # num_nodes = G1.number_of_nodes()
    # G2 = nx.read_gexf("dataset_G1.gexf")
    # print('g2读取完毕')
    # initial_network(G2, sa)
    # G3 = nx.read_gexf("dataset_G1.gexf")
    # print('g3读取完毕')
    # initial_network(G3, sa)
    # G4 = nx.read_gexf("dataset_G1.gexf")
    # print('g4读取完毕')
    # initial_network(G4, sa)
    # draw_param_compare()
    # draw_network_compare(paras)

