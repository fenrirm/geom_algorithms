import math
from matplotlib import pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w_in = 0
        self.w_out = 0

    def __repr__(self):
        return "(" + str(self.x) + "; " + str(self.y) + ")"


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.weight = 0
        self.to = end.x
        self.rotation = math.atan2(end.y - start.y, end.x - start.x)

    def __repr__(self):
        return str(edges.index(self))


def read_data(file_name_vertices, file_name_edges):
    vertices = []
    edges = []
    edges_input_array = open(file_name_edges).read().split()
    vertices_input_array = open(file_name_vertices).read().split()

    i = 0
    while i < len(vertices_input_array):
        x = int(vertices_input_array[i])
        y = int(vertices_input_array[i + 1])
        vertices.append(Point(x, y))
        i += 2

    i = 0
    while i < len(edges_input_array):
        start_point = vertices[int(edges_input_array[i])]
        end_point = vertices[int(edges_input_array[i + 1])]
        edges.append(Edge(start_point, end_point))
        i += 2
    return vertices, edges


def sum_weight(array):
    result = 0
    for edge in array:
        result = result + edge.weight
    return result


def leftmost_edge(array):
    array = sort_edges(array)
    return array[0]


def leftmost_unused(array):
    i = 0
    result = array[0]
    while i < len(array):
        if array[i].weight > 0:
            result = array[i]
            break
        i += 1
    return result


def sort_edges(array):
    return sorted(array, key=lambda edge: edge.rotation, reverse=True)


def create_chain(chain_num):
    current_v = 0
    while current_v != n - 1:
        new_in_chain = leftmost_unused(ordered_edges_out[current_v])
        chains[chain_num].append(new_in_chain)
        new_in_chain.weight -= 1
        current_v = vertices.index(new_in_chain.end)


def find(point):
    for p in range(0, num_chains):
        for e in chains[p]:
            if e.start.y < point.y < e.end.y:
                point_vector = Point(point.x - e.start.x, point.y - e.start.y)
                edge_vector = Point(e.end.x - e.start.x, e.end.y - e.start.y)
                if math.atan2(point_vector.y, point_vector.x) > math.atan2(edge_vector.y, edge_vector.x):
                    return create_list_of_edges_for_answer(chains[p - 1], chains[p], point)
    return []


def find_index(point):
    i = 0
    for vertex in vertices:
        if vertex == point:
            return i
        i = i + 1
    return 0


def create_list_of_edges_for_answer(prev_chain, chain, z):
    result = []
    result_new = []
    result.extend(prev_chain)
    result.extend(chain)
    vertices_in_graph = [0] * len(vertices)
    for element in chain:
        vertices_in_graph[find_index(element.end)] += 1
        vertices_in_graph[find_index(element.start)] += 1
    for element in prev_chain:
        vertices_in_graph[find_index(element.end)] += 1
        vertices_in_graph[find_index(element.start)] += 1
    for i in range(len(vertices_in_graph)):
        vertices_in_graph[i] //= 2
    vertices_in_graph[0] += 1
    vertices_in_graph[-1] += 1
    prev = 0
    for i in range(1, len(vertices)):
        if vertices_in_graph[i] > 1:
            if vertices[i].y > z.y:
                for edge in result:
                    if vertices[prev].y <= edge.start.y < vertices[i].y:
                        result_new.append(edge)
                return result_new
            else:
                prev = i

    return result_new


point_to_locate = Point(11, 11)

def plot():
    ax = plt.axes()

    i = 0
    for vertex in vertices:
        plt.annotate(i, (vertex.x, vertex.y), fontsize=20)
        plt.plot(vertex.x, vertex.y, marker="o", markersize=4, markerfacecolor="green")
        i += 1
    for edge in edges:
        ax.arrow(edge.start.x, edge.start.y,
                 edge.end.x - edge.start.x, edge.end.y - edge.start.y, head_width=0, head_length=0)
        plt.annotate(edge.weight,
                     xy=((edge.end.x + edge.start.x) / 2, (edge.end.y + edge.start.y) / 2),
                     xytext=(10, -10),
                     textcoords='offset points',
                     fontsize=14)

    plt.plot(point_to_locate.x, point_to_locate.y, marker="o", markersize=8, markerfacecolor="red")
    plt.show()


if __name__ == "__main__":
    vertices, edges = read_data("vertices.txt", "edges.txt")
    vertices = sorted(vertices, key=lambda point: point.y)

    edges_in = []
    edges_out = []

    for vertex in vertices:
        edges_in.insert(vertices.index(vertex), [])
        edges_out.insert(vertices.index(vertex), [])

    for edge in edges:
        from_idx = vertices.index(edge.start)
        to_idx = vertices.index(edge.end)
        edges_out[from_idx].append(edge)
        edges_in[to_idx].append(edge)
        edge.weight = 1

    n = len(vertices)

    for i in range(1, n - 1):
        vertices[i].w_in = sum_weight(edges_in[i])
        vertices[i].w_out = sum_weight(edges_out[i])
        edges_out[i] = sort_edges(edges_out[i])
        if vertices[i].w_in > vertices[i].w_out:
            edges_out[i][0].weight = vertices[i].w_in - vertices[i].w_out + 1

    for i in range(n - 1, 1, -1):
        vertices[i].w_in = sum_weight(edges_in[i])
        vertices[i].w_out = sum_weight(edges_out[i])
        edges_in[i] = sort_edges(edges_in[i])
        if vertices[i].w_out > vertices[i].w_in:
            edges_in[i][0].weight = vertices[i].w_out - vertices[i].w_in + edges_in[i][0].weight

    plot()
    chains = []
    num_chains = sum_weight(edges_out[0])

    ordered_edges_out = []
    for v in edges_out:
        v = sort_edges(v)
        ordered_edges_out.append(v)

    for j in range(num_chains):
        chains.insert(j, [])
        create_chain(j)

    for i, chain in enumerate(chains):
        print(f"Chain {i}: {vertices.index(chain[0].start)}", end="")
        for edge in chain:
            print(f" {vertices.index(edge.end)}", end="")
        print()
    result = find(point_to_locate)
    if not result:
        print("Not inside the graph")
    for edge in result:
        print(f" {find_index(edge.start)} {find_index(edge.end)} ", end="")
