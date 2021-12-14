import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tool import count_nodenum,count_SEIIRnodenum
from model import new_model,SEIIR_model
from GraphBuild import build_network, initial_network,build_ego_network,initial_SEIIRnetwork
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
plt.rcParams["font.family"] = "cursive"
# 确保 中文 和 -
plt.rcParams['font.sans-serif'] = ['times']
plt.rcParams['axes.unicode_minus'] = False

def start_diffusion(G, paras, t_list,num_nodes):
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
        new_model(G, paras, nums[-2], t)
    print('完成！')
    print(len(node_list))
    return node_list


def start_SEIIRdiffusion(G,t_list,num_nodes):
    node_list = []
    for t in range(len(t_list)):
        # 计算并存储当前各个节点数目
        nums = count_SEIIRnodenum(G)
        nums = [num / num_nodes for num in nums]
        print(t, ': ', nums)
        node_list.append(nums)
        SEIIR_model(G)
    print('完成！')
    print(len(node_list))
    return node_list

def draw_node_trend(node_list,t_list):
    """
    输出各类节点趋势
    :param G: 输入图
    :param beta: 感染率
    """
    # 整理数据
    df = pd.DataFrame(data=node_list, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    # 显示数据曲线
    df1 = df[['Si', 'E', 'I', 'R', 'Sa']]
    df1.plot(color=[color_dict.get(x) for x in df1.columns],
             style=[style_dict.get(x) for x in df1.columns], markersize=5)
    plt.ylabel('Ratio(%)')
    plt.xlabel('Time/h')
    plt.legend(loc='lower right')
    # plt.title('')
    # plt.savefig('10101931_12_05_01_02 nodes')
    plt.show()

    df2 = df[['tweet', 'read']]
    # 显示数据曲线
    df2.plot(color=[color_dict.get(x) for x in df2.columns],markersize=5)
    plt.ylabel('Ratio(%)')
    plt.xlabel('Time/h')
    plt.legend(loc='lower right')
    # plt.title('tweet and read percents')
    plt.show()
    # plt.savefig('10101931_tweet and read')


def draw_SEIIRnode_trend(node_list,t_list):
    """
    输出各类节点趋势
    :param G: 输入图
    :param beta: 感染率
    """
    # 整理数据
    df = pd.DataFrame(data=node_list, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    # 显示数据曲线
    df1 = df[['Si', 'E', 'I', 'R', 'Sa']]
    df1.plot(figsize=(8, 6), color=[color_dict.get(x) for x in df1.columns],
             style=[style_dict.get(x) for x in df1.columns])
    plt.ylabel('Ratio(%)')
    plt.xlabel('Time/h')
    plt.legend(loc='lower right')
    # plt.title('')
    # plt.savefig('10101931_12_05_01_02 nodes')
    plt.show()


def draw_param_compare():
    """
    输出参数对此实验
    :param G: 输入图
    :param beta: 感染率
    """
    t_list = np.linspace(1,40,40)
    # 设定传播步长
    node_list_1 = start_diffusion(G1, paras1, t_list,num_nodes)
    df1 = pd.DataFrame(data=node_list_1, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df1 = df1['tweet']
    node_list_2 = start_diffusion(G2, paras2, t_list, num_nodes)
    df2 = pd.DataFrame(data=node_list_2, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df2 = df2['tweet']
    node_list_3 = start_diffusion(G3, paras3, t_list, num_nodes)
    df3 = pd.DataFrame(data=node_list_3, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df3 = df3['tweet']
    node_list_4 = start_diffusion(G4, paras4, t_list,num_nodes)
    df4 = pd.DataFrame(data=node_list_4, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df4 = df4['tweet']
    # 显示数据曲线
    df1.plot(color='yellowgreen',style='^-',markersize=5)
    df2.plot(color='orange', style='o-',markersize=5)
    df3.plot(color='orangered', style='*-',markersize=6)
    df4.plot(color='darkred', style='s-',markersize=5)
    plt.ylabel('Ratio(%)')
    plt.xlabel('Time/h')
    plt.legend(['v1=0.05', 'v1=0.1', 'v1=0.2', 'v1=0.3'], loc='lower right')
    # plt.title('不同非转发者免疫速率下转发比例对比')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    # plt.savefig('param_value')
    plt.show()


def draw_network_compare(paras):
    """
    输出参数对此实验
    :param G: 输入图
    :param beta: 感染率
    """

    # 设定传播步长
    t_list = np.linspace(1, 50, 50)
    G1 = nx.read_gexf("dataset_G1.gexf")
    G2, num_nodes2 = build_network('ba',100000)
    G3, num_nodes3 = build_network('ws', 100000)
    # 初始化网络节点
    max_de1 = initial_network(G1)
    num_nodes1 = G1.number_of_nodes()
    print(num_nodes1)
    max_de2 = initial_network(G2)
    print(num_nodes2)
    max_de3 = initial_network(G3)
    print(num_nodes3)
    # 开始传播
    node_list1 = start_diffusion(G1, paras, t_list,num_nodes1)
    df1 = pd.DataFrame(data=node_list1, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df1 = df1['I']

    node_list2 = start_diffusion(G2, paras, t_list, num_nodes2)
    df2 = pd.DataFrame(data=node_list2, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df2 = df2['I']

    node_list3 = start_diffusion(G3, paras, t_list, num_nodes3)
    df3 = pd.DataFrame(data=node_list3, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df3 = df3['I']
    # 显示数据曲线
    df1.plot(color='orange', style='*-',markersize=5)
    df2.plot(color='orangered', style='o-',markersize=4)
    df3.plot(color='darkred', style='s-',markersize=4)
    plt.ylabel('Ratio(%)')
    plt.xlabel('Time/h')
    plt.legend(['Weibo network', 'BA network','WS network'], loc='center right')
    # plt.title('不同网络结构下的对比')
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # aaaaa.py 步骤一（替换sans-serif字体）
    plt.savefig('dataset_ba_ws_VSEIIR_model')
    plt.show()


def draw_model_compare(paras):
    G1 = nx.read_gexf("dataset_G1.gexf")
    print('g1读取完毕')
    initial_network(G1)
    num_nodes = G1.number_of_nodes()
    G2 = nx.read_gexf("dataset_G1.gexf")
    print('g2读取完毕')
    initial_SEIIRnetwork(G2)
    num_nodes = G2.number_of_nodes()

    t_list = np.linspace(1, 40, 40)
    node_list1 = start_diffusion(G1, paras, t_list, num_nodes)
    # draw_node_trend(node_list1, t_list)
    df1 = pd.DataFrame(data=node_list1, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet', 'read'])
    df1 = df1['I']

    node_list2 = start_SEIIRdiffusion(G2,t_list,num_nodes)
    # draw_SEIIRnode_trend(node_list2, t_list)
    df2 = pd.DataFrame(data=node_list2, index=t_list, columns=['Si', 'E', 'I', 'R', 'Sa', 'tweet'])
    df2 = df2['I']

    df1.plot(color='orange', style='*-',markersize=5)
    df2.plot(color='orangered', style='o-',markersize=4)
    plt.ylabel('Ratio(%)')
    plt.xlabel('Time/h')
    plt.legend(['Proposed model', 'SEIIR model'], loc='center right')
    plt.show()

if __name__ == '__main__':
    # N = 10000  # 总人数
    # i = 1  # 感染者人数
    # sa_num = N*0.05  # 活跃者人数

    # 非活跃者人数
    # si = N - i - sa
    # 参数 [pubtime, r, fi, fa, v1, v2, v3]
    paras = [12, 0.5, 1/8, 1/2, 0.1, 0.2, 0.2]
    # 各个节点数目列表

    # 节点颜色
    color_dict = {'Si': 'blue', 'E': 'orange', 'I': 'red', 'R': 'black', 'Sa': 'green',
                  'tweet': 'darkred', 'read': 'orangered'}
    style_dict = {'Si': '-', 'E': '-.', 'I': '--', 'R': 'o-', 'Sa': '+-',
                  'tweet': '*-', 'read': 's-'}
    # # 创建网络
    # #G, num_nodes = build_network('dataset',20000)
    # G = nx.read_gexf("dataset_G1.gexf")
    # # # G, num_nodes = build_ego_network(100000,5)

    # # 初始化网络节点
    # num_nodes = G.number_of_nodes()
    # sa_num = int(num_nodes * 0.1)
    # max_de = initial_network(G)
    # print('该网络共有', num_nodes, '个点')
    # # # 开始传播
    # t_list = np.linspace(1,40,40)
    # print('步长为：', len(t_list))
    # node_list = start_diffusion(G, paras, t_list ,num_nodes)
    # # 输出节点趋势图
    # draw_node_trend(node_list,t_list)

    #
    # paras1 = [12, 0.5, 1/8, 1/2, 0.05, 0.3, 0.3]
    # paras2 = [12, 0.5, 1/8, 1/2, 0.1, 0.3, 0.3]
    # paras3 = [12, 0.5, 1/8, 1/2, 0.2, 0.3, 0.3]
    # paras4 = [12, 0.5, 1/8, 1/2, 0.3, 0.3, 0.3]
    # G1 = nx.read_gexf("dataset_G1.gexf")
    # print('g1读取完毕')
    # max_de1 = initial_network(G1)
    # num_nodes = G1.number_of_nodes()
    # G2 = nx.read_gexf("dataset_G1.gexf")
    # print('g2读取完毕')
    # max_de2 = initial_network(G2)
    # G3 = nx.read_gexf("dataset_G1.gexf")
    # print('g3读取完毕')
    # max_de3 = initial_network(G3)
    # G4 = nx.read_gexf("dataset_G1.gexf")
    # print('g4读取完毕')
    # max_de4= initial_network(G4)
    # draw_param_compare()

    # draw_network_compare(paras)

    draw_model_compare(paras)