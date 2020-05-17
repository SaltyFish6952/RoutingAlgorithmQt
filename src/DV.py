import numpy as np

infinity = 10000
point_router_list = []
count = 0


class Node:

    def __init__(self, source, destination, neighbor, next, cost):
        self.source = source
        self.destination = destination
        self.neighbor = neighbor
        self.next = next
        self.cost = cost


def create_array(n, value):
    array = []

    for i in range(n):
        array.append(value)

    return array


def init(n, adjacentMatrix):
    global point_router_list
    global count

    for i in range(n):

        next_point = []
        neighbor = []

        for j in range(n):

            if adjacentMatrix[i][j] != infinity:
                next_point.append(j)
                neighbor.append(j)
            else:
                next_point.append("null")
                neighbor.append(-1)

        point = Node(i, [k for k in range(n)], neighbor, next_point, adjacentMatrix[i])



        point_router_list.append(point)

    # print(point_matrix_list)


def send_msg(source_index, destination_index):
    global count

    flag = False

    source_point = point_router_list[source_index]
    destination_point = point_router_list[destination_index]

    for i in range(count):

        a = destination_point.cost[source_point.source] + source_point.cost[i]
        b = destination_point.cost[i]

        if destination_point.cost[source_point.source] + source_point.cost[i] < destination_point.cost[i]:

            # if destination_point.neighbor[i] == -1:
            #     destination_point.neighbor[i] = i

            new_distance = destination_point.cost[source_point.source] + source_point.cost[i]
            destination_point.cost[i] = new_distance

            destination_point.next[i] = source_point.source
            # destination_point.next[i] = source_point.source
            flag = True

    return flag


def calc_router(n, adjacentMatrix):
    global point_router_list
    global count
    count = n

    point_router_list.clear()

    init(count, adjacentMatrix)

    isUpdate = create_array(count, 0)
    while True:

        for i in range(count):

            for j in range(len(point_router_list[i].neighbor)):

                if point_router_list[i].neighbor[j] != -1:
                    if send_msg(i, point_router_list[i].neighbor[j]):
                        isUpdate[i] = 1
                    else:
                        isUpdate[i] = 0

        flag = True

        for i in range(count):
            if isUpdate[i] == 1:
                flag = False

        if flag:
            print('added-path')

            return point_router_list



