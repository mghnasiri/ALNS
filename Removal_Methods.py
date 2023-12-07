import networkx as nx
import random



def Random_Removal(G, tour,removal_count):
    """
    Randomly remove a set number of nodes from the tour.
    
    :param tour: Current TSP tour as a list of nodes.
    :param removal_count: Number of nodes to remove.
    :return: A new tour with nodes removed and a list of removed nodes.
    """
    if removal_count >= len(tour) - 1:
        raise ValueError("Removal count must be less than the number of nodes in the tour.")

    # Exclude the first and last node if they are the same (start/end node)
    removable_nodes = tour[1:-1] if tour[0] == tour[-1] else tour
    removed_nodes = set(random.sample(removable_nodes, removal_count))
    new_tour = [node for node in tour if node not in removed_nodes]

    return new_tour, list(removed_nodes)

def Worst_Removal(G, tour, removal_count):
    
    def calculate_edge_cost_increase(G, tour):
        """
            Calculate the cost increase for each edge if it were removed from the tour. 
            :param G: Graph representing the TSP.
            :param tour: Current TSP tour as a list of nodes.
            :return: A list of tuples (edge, cost_increase).
        """
        edge_cost_increase = []
        for i in range(len(tour) - 1):
                current_cost = G[tour[i]][tour[i+1]]['length']
                next_node = tour[i+2] if i < len(tour) - 2 else tour[0]
                new_cost = G[tour[i]][next_node]['length']
                cost_increase = new_cost - current_cost
                edge_cost_increase.append(((tour[i], tour[i+1]), cost_increase))
            
        return edge_cost_increase
    
    """
    Remove the 'worst' edges from the tour.    
    :param G: Graph representing the TSP.
    :param tour: Current TSP tour as a list of nodes.
    :param removal_count: Number of edges to remove.
    :return: A new tour with the worst edges removed.
    """
    edge_cost_increase = calculate_edge_cost_increase(G, tour)
    edges_to_remove = sorted(edge_cost_increase, key=lambda x: x[1], reverse=True)[:removal_count]

    removed_nodes = set()
    # Remove the selected edges and rebuild the tour
    for edge, _ in edges_to_remove:
        if edge[0] in tour and edge[1] in tour:
                index = tour.index(edge[0])
                removed_node = tour.pop(index + 1)
                removed_nodes.add(removed_node)
    return tour, list(removed_nodes)


def Shaw_Removal(G, tour, removal_count):
    def calculate_relatedness(G, node, other_node):
        """
        Calculate a relatedness score between two nodes. 
        This can be based on distance, demand similarity, or other criteria.
    
        :param G: Graph representing the TSP.
        :param node: The node for which to calculate relatedness.
        :param other_node: The other node to compare against.
        :return: A relatedness score (lower means more related).
        """
        # Example: Using Euclidean distance as the relatedness measure
        distance = G[node][other_node]['length']
        return distance
    
    """
    Remove a set of related nodes from the tour using the Shaw Removal heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current TSP tour as a list of nodes.
    :param removal_count: Number of nodes to remove.
    :return: A new tour with nodes removed.
    """
    if removal_count >= len(tour) - 1:
        raise ValueError("Removal count must be less than the number of nodes in the tour.")

    # Randomly select a seed node to base the removal around
    seed_node = random.choice(tour[1:-1])  # Exclude start/end node if it's the same

    # Calculate relatedness of all other nodes to the seed node
    relatedness_scores = [(node, calculate_relatedness(G, seed_node, node)) for node in tour if node != seed_node]
    relatedness_scores.sort(key=lambda x: x[1])

    # Select the nodes with the lowest relatedness scores (most related) to remove
    nodes_to_remove = set([node for node, _ in relatedness_scores[:removal_count]])
    new_tour = [node for node in tour if node not in nodes_to_remove]
    
    return new_tour,nodes_to_remove

def Related_Removal(G, tour, removal_count):
    def calculate_relatedness(G, node, other_node):
        """
        Calculate a relatedness score between two nodes based on certain criteria.

        :param G: Graph representing the TSP.
        :param node: The node for which to calculate relatedness.
        :param other_node: The other node to compare against.
        :return: A relatedness score (lower means more related).
        """
        # Example: Using Euclidean distance combined with other criteria
        distance = G[node][other_node]['length']
        # You can incorporate more criteria here to define 'relatedness'
        return distance
    """
    Remove a set of related nodes from the tour using the Related Removal heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current TSP tour as a list of nodes.
    :param removal_count: Number of nodes to remove.
    :return: A new tour with nodes removed.
    """
    if removal_count >= len(tour) - 1:
        raise ValueError("Removal count must be less than the number of nodes in the tour.")

    # Randomly select a seed node to base the removal around
    seed_node = random.choice(tour[1:-1])  # Exclude start/end node if it's the same

    # Calculate relatedness of all other nodes to the seed node
    relatedness_scores = [(node, calculate_relatedness(G, seed_node, node)) for node in tour if node != seed_node]
    relatedness_scores.sort(key=lambda x: x[1])

    # Select the nodes with the lowest relatedness scores (most related) to remove
    nodes_to_remove = set([node for node, _ in relatedness_scores[:removal_count]])
    new_tour = [node for node in tour if node not in nodes_to_remove]


    return new_tour,nodes_to_remove

def Route_Based_Removal(G,  tour, removal_count):

    """
    Remove a contiguous segment of the tour.
    
    :param tour: Current TSP tour as a list of nodes.
    :param removal_length: Length of the tour segment to remove.
    :return: A new tour with a segment removed.
    """
    if removal_count >= len(tour) - 1:
        raise ValueError("Removal length must be less than the number of nodes in the tour.")

    start_index = random.randint(1, len(tour) - removal_count - 1)  # Excluding the first and last node
    end_index = start_index + removal_count

    # Remove the segment from the tour
    new_tour = tour[:start_index] + tour[end_index:]

    # Extract the removed segment for reference
    removed_segment = tour[start_index:end_index]

    return new_tour, removed_segment 
