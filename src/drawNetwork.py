import networkx as nw
import random as rand
import math
import numpy as np
from matplotlib import pyplot as plt


point_dict = {}
neighbor_dict = {}
R = 50
infinity = 10000
X_MAX = 500
Y_MAX = 500


def check_if_same_point(x, y):
    global point_dict
    for item in point_dict:
        if item is not None:
            if (point_dict[item]['x'] == x) or (point_dict[item]['y'] == y):
                return True

    return False


def make_points():
    global point_dict
    points_count = rand.randint(200, 400)

    for point in range(points_count):
        x = rand.randint(0, X_MAX)
        y = rand.randint(0, Y_MAX)

        while check_if_same_point(x, y):
            x = rand.randint(0, X_MAX)
            y = rand.randint(0, Y_MAX)

        point_dict.update({point: {'x': x, 'y': y}})


def get_neighbor():
    global point_dict, neighbor_dict
    AdjcentMatrix = np.full((len(point_dict), len(point_dict)), infinity)

    for point_i in range(len(point_dict)):

        point_i_x = point_dict[point_i]['x']
        point_i_y = point_dict[point_i]['y']

        for point_j in range(len(point_dict)):

            if point_dict[point_j]['x'] == point_i_x and point_dict[point_j]['y'] == point_i_y:
                AdjcentMatrix[point_i][point_j] = 0
                continue

            distance = math.sqrt((point_dict[point_j]['x'] - point_i_x) ** 2
                                 + (point_dict[point_j]['y'] - point_i_y) ** 2)

            if distance <= R:
                if point_i in neighbor_dict.keys():
                    this_neighbor_list = neighbor_dict[point_i]
                else:
                    this_neighbor_list = []
                this_neighbor_list.append(point_j)
                neighbor_dict.update({point_i: this_neighbor_list})
                AdjcentMatrix[point_i][point_j] = 1

    return AdjcentMatrix


def createGraph():
    global graph, point_dict, neighbor_dict
    point_dict.clear()
    neighbor_dict.clear()
    plt.figure(figsize=(20, 15), dpi=50)
    graph = nw.Graph()

    make_points()
    AdjcentMatrix = get_neighbor()

    for i in range(len(point_dict)):
        graph.add_node(i)

    for i in neighbor_dict:
        point_edge = neighbor_dict[i]

        for j in range(len(point_edge)):
            graph.add_edge(i, point_edge[j])

    pos = []

    for i in range(len(point_dict)):
        pos.append((point_dict[i]['x'], point_dict[i]['y']))

    nw.draw(graph, pos=pos, node_size=200, with_labels=range(len(point_dict)), font_size=30)

    plt.savefig('graph_total')

    plt.cla()
    graph.clear()

    return AdjcentMatrix, len(point_dict)


def drawResult(ways):
    global graph, point_dict, neighbor_dict
    graph = nw.Graph()
    plt.cla()

    for i in range(len(point_dict)):
        graph.add_node(i)

    for i in neighbor_dict:
        point_edge = neighbor_dict[i]

        for j in range(len(point_edge)):
            graph.add_edge(i, point_edge[j])

    tuple_way_list = []

    for i in range(len(ways) - 1):
        tuple_way_list.append((ways[i], ways[i + 1]))
    pos = []

    for i in range(len(point_dict)):
        pos.append((point_dict[i]['x'], point_dict[i]['y']))

    nw.draw(graph, pos=pos, node_size=200, with_labels=range(len(point_dict)), font_size=30)
    nw.draw_networkx_edges(graph, pos, edgelist=tuple_way_list, width=8, alpha=0.5, edge_color='r')
    plt.savefig('graph_total')
#
# # plt.show()
# plt.ion()
# v0 = input('请输入需要查找的节点：')
#
# v0 = int(v0)
#
# v1 = input('请输入需要到达的节点：')
#
# v1 = int(v1)
#
# choice = input('1.DV算法  2.LS算法\n     请选择需要计算的算法：')
#
# choice = int(choice)
#
# if choice == 1:
#
#     # dv
#     print("hehehe")
#
#     router_list = dv_new.calc_router(len(point_dict), AdjcentMatrix)
#
#     for i in range(len(router_list)):
#         print('节点 {0} 路由表如下：'.format(i))
#         print('目的地\t下一跳\t路径长度')
#         for j in range(len(router_list[i].neighbor)):
#             print('{0}\t{1}\t{2}'.format(router_list[i].destination[j], router_list[i].next[j], router_list[i].cost[j]))
#
#     # dv.init(len(point_dict), AdjcentMatrix)
#     # res = dv.calc_router(v0)
#     #
#     # distance = res[0]
#     # path = res[1]
#
#     # print(distance)
#     # print(path)
#
# elif choice == 2:
#     # ls
#
#     res = ls.dijkstra(len(point_dict), AdjcentMatrix, v0)
#
#     distance = res[0]
#     path = res[1]
#
#     print(distance)
#     print(path)
#
#     plt.figure(figsize=(20, 15), dpi=50)
#     graph = nw.Graph()
#
#     for i in range(len(point_dict)):
#         graph.add_node(i)
#
#     ways = ls.get_ways(v0, v1, path)
#
#     for i in range(len(ways) - 1):
#         graph.add_edge(ways[i], ways[i + 1])
#
#     print('从 {0} 节点到 {1} 节点的最短路径为：{2}'.format(v0, v1, distance[v1]))
#
#     nw.draw(graph, pos=pos, node_size=500, with_labels=range(len(point_dict)), font_size=20)
#
#     plt.show()
