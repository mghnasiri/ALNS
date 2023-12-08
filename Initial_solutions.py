import networkx as nx
import random
from itertools import combinations



def Nearest_Neighbor_Heuristic(G,start_node):
    #Generate an initial solution for TSP using the Nearest Neighbor Heuristic.
    #:param G: A NetworkX graph with cities as nodes and edges with 'length' attribute.
    #:return: A tour as a list of city indices.
    nodes = list(G.nodes)
    current_city = start_node
    tour = [current_city]
    unvisited = set(nodes)
    unvisited.remove(current_city)

    while unvisited:     # Loop until all cities are visited
        nearest_city = min(unvisited, key=lambda city: G[current_city][city]['length'])
        tour.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
    
    tour.append(start_node)  # Return to the depot at the end of the tour
    return tour 

def  Christofides_Algorithm(G,start_node):
    
    def create_minimum_spanning_tree(G):
    #""" Create a Minimum Spanning Tree (MST) from the graph. """
    # Convert the directed graph to an undirected graph
        G_undirected = G.to_undirected()
        # Compute the minimum spanning tree on the undirected graph
        mst = nx.minimum_spanning_tree(G_undirected)
        return mst
    
    def find_odd_degree_vertices(mst):
        """
        Find vertices with odd degree in the MST.
        :param mst: A Minimum Spanning Tree (MST) represented as a NetworkX graph.
        :return: A list of vertices (nodes) that have an odd degree in the MST.
        """
        odd_degree_vertices = []  # Initialize an empty list to store vertices with odd degree
        # Iterate through each vertex in the MST
        for vertex in mst.nodes():
            # Check if the degree of the vertex is odd
            if mst.degree(vertex) % 2 != 0:
                # If the degree is odd, add the vertex to the list
                odd_degree_vertices.append(vertex)
        return odd_degree_vertices  # Return the list of vertices with odd degree

    def form_eulerian_circuit(multigraph, start_node):
        """ Form a Eulerian circuit on the multigraph. """
        return list(nx.eulerian_circuit(multigraph, source=start_node))

    def approximate_min_weight_matching(G, odd_degree_vertices):
        """ 
        Create an approximate minimum weight perfect matching. 
        This is a placeholder and does not guarantee minimum weight.
        """
        random.shuffle(odd_degree_vertices)
        return list(zip(odd_degree_vertices[0::2], odd_degree_vertices[1::2]))

    def combine_edges(mst, mwm):
        """ Combine the edges of the MST and the edges from the perfect matching. """
        multigraph = nx.MultiGraph(mst)
        multigraph.add_edges_from(mwm)
        return multigraph

    
    """ Implement Christofides' Algorithm. """
    mst = create_minimum_spanning_tree(G)
    odd_degree_vertices = find_odd_degree_vertices(mst)
    mwm = approximate_min_weight_matching(G, odd_degree_vertices)
    multigraph = combine_edges(mst, mwm)
    eulerian_circuit = form_eulerian_circuit(multigraph, start_node)

        # Convert the Eulerian circuit to a Hamiltonian circuit (TSP tour)
    tour = []
    visited = set()
    for u, v in eulerian_circuit:
        if u not in visited:
            tour.append(u)
            visited.add(u)
    tour.append(tour[0])  # Return to the start node
    
    return tour

def Minimum_Spanning_Tree_MST_Based_Heuristic(G,start_node):
    def create_minimum_spanning_tree(G):
    #""" Create a Minimum Spanning Tree (MST) from the graph. """
    # Convert the directed graph to an undirected graph
        G_undirected = G.to_undirected()
        # Compute the minimum spanning tree on the undirected graph
        mst = nx.minimum_spanning_tree(G_undirected)
        return mst

    mst = create_minimum_spanning_tree(G)
    tour = list(nx.dfs_preorder_nodes(mst,start_node))
    # Add the start node at the end to complete the tour
    tour.append(start_node)
    return tour

def Savings_Algorithm(G, start_node):
    
    def calculate_savings(G, start_node):
        """ Calculate savings for combining two routes into one. """
        savings = {}
        for i, j in combinations(G.nodes(), 2):
            if i != start_node and j != start_node:
                cost_separate = G[start_node][i]['length'] + G[start_node][j]['length']
                cost_combined = G[i][j]['length']
                savings[(i, j)] = cost_separate - cost_combined
        
        return savings

    """ Apply the Savings Algorithm to create routes. """
    routes = [[start_node, node, start_node] for node in G.nodes() if node != start_node]
    savings = calculate_savings(G, start_node)
    sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)

    for (i, j), _ in sorted_savings:
        route_i = None
        route_j = None
        for route in routes:
            if i in route:
                route_i = route
            if j in route:
                route_j = route
        if route_i is not route_j and route_i[1] == i and route_j[-2] == j:
            # Combine routes
            combined_route = route_j[:-1] + route_i[1:]
            routes.remove(route_i)
            routes.remove(route_j)
            routes.append(combined_route)

    return routes

def Cheapest_Insertion_Ini(G,start_node):
    def find_cheapest_insertion(G, tour):
        """ Find the cheapest node and position to insert into the existing tour. """
        min_increase = float('inf')
        cheapest_node = None
        position = 0
        for node in set(G.nodes()) - set(tour):
            for i in range(len(tour) - 1):
                increase = (G[tour[i]][node]['length'] + 
                            G[node][tour[i + 1]]['length'] - 
                            G[tour[i]][tour[i + 1]]['length'])
                if increase < min_increase:
                    min_increase = increase
                    cheapest_node = node
                    position = i + 1
        return cheapest_node, position
    
    """ Generate a TSP tour using the Cheapest Insertion heuristic. """
    # Initialize tour with the start node and its nearest neighbor
    nearest_neighbor = min(G[start_node], key=lambda k: G[start_node][k]['length'])
    tour = [start_node, nearest_neighbor, start_node]

    # Repeat until all nodes are in the tour
    while len(tour) < len(G.nodes()) + 1:
        node, position = find_cheapest_insertion(G, tour)
        tour.insert(position, node)
    
    return tour

def  Farthest_Insertion(G,start_node):
    
    def find_farthest_node(G, subset):
        """ Find the farthest node from the subset of nodes already in the tour. """
        farthest_node = None
        max_distance = -1
        for node in set(G.nodes()) - set(subset):
            for sub_node in subset:
                distance = G[node][sub_node]['length']
                if distance > max_distance:
                    max_distance = distance
                    farthest_node = node
        return farthest_node
    
    def find_optimal_insertion(G, tour, node):
        """ Find the optimal position to insert the node into the existing tour. """
        min_increase = float('inf')
        position = 0
        for i in range(len(tour) - 1):
            increase = (G[tour[i]][node]['length'] + 
                        G[node][tour[i + 1]]['length'] - 
                        G[tour[i]][tour[i + 1]]['length'])
            if increase < min_increase:
                min_increase = increase
                position = i + 1
        return position

    """ Generate a TSP tour using the Farthest Insertion heuristic. """
    # Initialize tour with the start node and its nearest neighbor
    nearest_neighbor = min(G[start_node], key=lambda k: G[start_node][k]['length'])
    tour = [start_node, nearest_neighbor, start_node]
    # Repeat until all nodes are in the tour
    while len(tour) < len(G.nodes()) + 1:
        farthest_node = find_farthest_node(G, tour)
        position = find_optimal_insertion(G, tour, farthest_node)
        tour.insert(position, farthest_node)
        
    return tour

def  Randomized_Heuristics(G,start_node):
    """ Generate a TSP tour using a randomized heuristic. """
    tour = list(G.nodes())
    random.shuffle(tour)  # Randomly shuffle the order of nodes

    # If the start_node is specified and not the first node,
    # move it to the beginning of the tour
    if start_node in tour and start_node != tour[0]:
        tour.remove(start_node)
        tour.insert(0, start_node)

    # Add the start node at the end to complete the tour
    tour.append(start_node)
    return tour




