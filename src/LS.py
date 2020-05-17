MaxWeight = 10000


def create_array(n, value):
    array = []

    for i in range(n):
        array.append(value)

    return array


def dijkstra(n, adjcentMatrix, v0):
    u = 0
    minDis = 0

    s = create_array(n, 0)
    distance = create_array(n, MaxWeight)
    path = create_array(n, 0)

    for i in range(n):

        distance[i] = adjcentMatrix[v0][i]

        s[i] = 0

        if (i != v0) and (distance[i] < MaxWeight):
            path[i] = v0
        else:
            path[i] = -1

    s[v0] = 1

    for i in range(1, n):

        minDis = MaxWeight
        for j in range(n):

            if (s[j] == 0) and (distance[j] < minDis):
                u = j
                minDis = distance[j]

        # if minDis == MaxWeight:
        #     return distance, path

        s[u] = 1

        for j in range(n):

            if (s[j] == 0) and (adjcentMatrix[u][j] < MaxWeight) and ((distance[u] + adjcentMatrix[u][j]) < distance[j]):
                distance[j] = distance[u] + adjcentMatrix[u][j]
                path[j] = u

    return distance, path


def get_ways(v0, v1, path):
    curr = v1
    track = [curr]

    while curr != v0:
        curr = path[curr]
        if curr == -1:
            return
        track.append(curr)

    track.reverse()
    return track
