import networkx as nx
from matplotlib import pyplot as plt

options = {
    "with_labels": True,
    "node_size": 300,
    "node_color": "lightblue",
    "linewidths": 1.5,
    "width": 1.5,
    "edgecolors": "black",
    "font_size": 10,
    "font_color": "black",
    "font_weight": "normal",
    "font_family": "sans-serif",
}

layout_params = {
    "k": 1,
    "iterations": 50,
}


def calculate_weight(distance, time, consumption):
    return round((distance * 0.2) + (((distance / 100) * consumption) * 0.2) + (time * 0.6), 2)


locals = {
    "A1": (41.320855, -8.145473),  # 4615 Hotel
    "M1": (41.343831, -8.248757),  # Igreja de São Vicente de Sousa
    "M2": (41.312157, -8.236581),  # Igreja do Salvador de Unhão
    "M3": (41.314833, -8.198791),  # Igreja de Santa Maria de Airães
    "M4": (41.304822, -8.181841),  # Igreja de São Mamede de Vila Verde
    "M5": (41.279507, -8.253011),  # Igreja do Salvador de Aveleda
    "M6": (41.382566, -8.225727),  # Mosteiro de Santa Maria de Pombeiro
}

roads_data = {
    ("A1", "M3", 5.5, 8, 8.5),
    ("A1", "M4", 5.1, 7, 6.8),
    ("A1", "M6", 12.5, 17, 7),
    ("M6", "M1", 7.7, 12, 6.7),
    ("M6", "M2", 10.9, 14, 4.8),
    ("M6", "M3", 11.2, 14, 9.2),
    ("M1", "M3", 8.3, 13, 5.5),
    ("M1", "M2", 5.6, 8, 5.2),
    ("M2", "M3", 5.4, 8, 7.1),
    ("M2", "M5", 6, 8, 5.9),
    ("M5", "M3", 7.5, 11, 5.3),
    ("M5", "M4", 11.2, 14, 7.5),
    ("M4", "M3", 3.6, 6, 6.3),
}

roads = {
    (road[0], road[1], calculate_weight(road[2], road[3], road[4])) for road in roads_data
}


def create_network():
    graph = nx.Graph()

    for local in locals:
        graph.add_node(local)

    for road in roads:
        graph.add_weighted_edges_from([(road[0], road[1], road[2])])

    return graph


def transitive_closure(graph):
    transitive_graph = nx.transitive_closure(graph)
    return transitive_graph


def check_dirac_theorem(graph):
    n = graph.number_of_nodes()
    if n < 3:
        return False, "Graph has less than 3 vertices"

    for node in graph.nodes():
        if graph.degree(node) < n / 2:
            return False, f"Vertex {node} violates Dirac's condition"

    return True, "Graph satisfies Dirac's condition and is Hamiltonian"


def check_ore_theorem(graph):
    n = graph.number_of_nodes()
    if n < 3:
        return False, "Graph has less than 3 vertices"

    non_adjacent_pairs = [(u, v) for u in graph.nodes() for v in graph.nodes() if u != v and not graph.has_edge(u, v)]

    for u, v in non_adjacent_pairs:
        if graph.degree(u) + graph.degree(v) < n:
            return False, f"Pair ({u}, {v}) violates Ore's condition"

    return True, "Graph satisfies Ore's condition and is Hamiltonian"


def shortest_path_from_accommodation_to_furthest_local(network, accommodation):
    max_distance = 0
    farthest_monument = None

    for local in locals:
        distance = nx.shortest_path_length(network, source=accommodation, target=local, weight='weight')
        if distance > max_distance:
            max_distance = distance
            farthest_monument = local

    shortest_path = nx.shortest_path(network, source=accommodation, target=farthest_monument, weight='weight')

    return farthest_monument, max_distance, shortest_path


def shortest_path_between_every_two_locations(network):
    shortest_paths = dict(nx.all_pairs_dijkstra_path(network, weight='weight'))
    shortest_distances = dict(nx.all_pairs_dijkstra_path_length(network, weight='weight'))

    for source in shortest_paths:
        for target in shortest_paths[source]:
            print(f"Shortest route from {source} to {target}:")
            print(f"Path: {shortest_paths[source][target]}")
            print(f"Total distance: {shortest_distances[source][target]:.2f}")
            print()


def tsp_minimum_cost_cycle(graph):
    tsp_cycle = nx.approximation.traveling_salesman_problem(graph, cycle=True, weight='weight')
    total_cost = 0
    for u, v in zip(tsp_cycle, tsp_cycle[1:] + [tsp_cycle[0]]):
        edge_data = graph.get_edge_data(u, v)
        if edge_data is None:
            continue
        total_cost += edge_data['weight']
    return tsp_cycle, total_cost


def draw_networks(network):
    filename = f'network.png'

    pos = nx.spring_layout(network, **layout_params)

    nx.draw(network, pos, **options)

    plt.savefig(filename, dpi=300)
    plt.close()


def draw_tsp(network, path):
    filename = f'tsp.png'

    pos = nx.spring_layout(network, **layout_params)

    nx.draw(network, pos, **options)

    nx.draw_networkx_edges(network, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
                           edge_color='r', width=2.0)

    plt.savefig(filename, dpi=300)
    plt.close()


def main():
    network = create_network()

    print("Adjacency matrix:")
    print(nx.to_numpy_array(network))
    print("\n")

    print("Transitive Closure")
    print(nx.to_numpy_array(transitive_closure(network)))
    print("\n")

    print("Dirac's Theorem:")
    satisfies_dirac, dirac_message = check_dirac_theorem(network)
    print(satisfies_dirac, dirac_message)
    print("\n")

    print("Ore's Theorem:")
    satisfies_ore, ore_message = check_ore_theorem(network)
    print(satisfies_ore, ore_message)
    print("\n")

    # Ex. 2. a)
    farthest_monument, max_distance, shortest_path = shortest_path_from_accommodation_to_furthest_local(network, "A1")
    print("Farthest monument:", farthest_monument)
    print(f"Distance: {max_distance:.2f}")
    print("Shortest path:", shortest_path)
    print("\n")

    # Ex. 2. b)
    shortest_path_between_every_two_locations(network)
    print("\n")

    # Ex. 3. c)
    path, cost = tsp_minimum_cost_cycle(network)
    print("Minimum cost Hamiltonian cycle starting at A1:")
    print(f"Path: {path}")
    print(f"Total cost: {cost:.2f}")
    print("\n")

    draw_networks(network)
    draw_tsp(network, path)


if __name__ == '__main__':
    main()
