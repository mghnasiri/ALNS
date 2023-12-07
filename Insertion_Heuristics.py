import random
import networkx as nx


def Basic_Insertion(G,tour,removed_nodes):
    """
    Reinsert the removed nodes into the tour using the basic insertion heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current partial TSP tour.
    :param removed_nodes: List of nodes to be reinserted.
    :return: Updated TSP tour with nodes reinserted.
    """
    for node_to_insert in removed_nodes:
        min_increase = float('inf')
        best_position = 0

        for i in range(1, len(tour)):
            increase = G[tour[i-1]][node_to_insert]['length'] + G[node_to_insert][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
            if increase < min_increase:
                min_increase = increase
                best_position = i

        tour.insert(best_position, node_to_insert)

    return  tour

def Regret_2_Heuristic(G, tour, removed_nodes):
    def calculate_regret(G, tour, node_to_insert):
        """
        Calculate the regret value of not inserting the node at the best and second-best positions.
    
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param node_to_insert: Node to be inserted.
        :return: Regret value and the best position for insertion.
        """
        min_increase = float('inf')
        second_min_increase = float('inf')
        best_position = 0
        for i in range(1, len(tour)):
            increase = G[tour[i-1]][node_to_insert]['length'] + G[node_to_insert][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
            if increase < min_increase:
                second_min_increase = min_increase
                min_increase = increase
                best_position = i
            elif increase < second_min_increase:
                second_min_increase = increase

        regret = second_min_increase - min_increase
        return regret, best_position

    """
    Reinsert the removed nodes into the tour using the Regret-2 heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current partial TSP tour.
    :param removed_nodes: List of nodes to be reinserted.
    :return: Updated TSP tour with nodes reinserted.
    """
    while removed_nodes:
        max_regret = -float('inf')
        node_to_insert = None
        insert_position = None

        for node in removed_nodes:
            regret, position = calculate_regret(G, tour, node)
            if regret > max_regret:
                max_regret = regret
                node_to_insert = node
                insert_position = position

        tour.insert(insert_position, node_to_insert)
        removed_nodes.remove(node_to_insert)

    return  tour

def Regret_3_Heuristic (G, tour, removed_nodes):
        
    def calculate_regret_3(G, tour, node_to_insert):
            """
            Calculate the regret value of not inserting the node at the best, second-best, and third-best positions.
    
            :param G: Graph representing the TSP.
            :param tour: Current partial TSP tour.
            :param node_to_insert: Node to be inserted.
            :return: Regret value and the best position for insertion.
            """
            insertion_costs = []
            for i in range(1, len(tour)):
                increase = G[tour[i-1]][node_to_insert]['length'] + G[node_to_insert][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
                insertion_costs.append((increase, i))

            insertion_costs.sort(key=lambda x: x[0])
            if len(insertion_costs) < 3:
                # If there are less than 3 positions, the regret is just the difference between the available options
                regret = insertion_costs[-1][0] - insertion_costs[0][0]
                best_position = insertion_costs[0][1]
            else:
                # Regret is the difference in cost between the third-best and the best positions
                regret = insertion_costs[2][0] - insertion_costs[0][0]
                best_position = insertion_costs[0][1]
        
            return regret, best_position
        
    """
    Reinsert the removed nodes into the tour using the Regret-3 heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current partial TSP tour.
    :param removed_nodes: List of nodes to be reinserted.
    :return: Updated TSP tour with nodes reinserted.
    """
    while removed_nodes:
        max_regret = -float('inf')
        node_to_insert = None
        insert_position = None

        for node in removed_nodes:
            regret, position = calculate_regret_3(G, tour, node)
            if regret > max_regret:
                max_regret = regret
                node_to_insert = node
                insert_position = position

        tour.insert(insert_position, node_to_insert)
        removed_nodes.remove(node_to_insert)
    
    return  tour


def Regret_N_Heuristic(G, tour, removed_nodes, N=5):
    
    def calculate_regret_n(G, tour, node_to_insert, N):
        """
        Calculate the regret value of not inserting the node at the best up to N-th best positions.
    
        :param G: Graph representing the TSP.
     :param tour: Current partial TSP tour.
        :param node_to_insert: Node to be inserted.
     :param N: Number of positions to consider for regret calculation.
        :return: Regret value and the best position for insertion.
        """
        insertion_costs = []
        for i in range(1, len(tour)):
            increase = G[tour[i-1]][node_to_insert]['length'] + G[node_to_insert][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
            insertion_costs.append((increase, i))

        insertion_costs.sort(key=lambda x: x[0])
        regret = sum(cost for cost, _ in insertion_costs[:N]) - N * insertion_costs[0][0]
        best_position = insertion_costs[0][1]

        return regret, best_position


    """
    Reinsert the removed nodes into the tour using the Regret-N heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current partial TSP tour.
    :param removed_nodes: List of nodes to be reinserted.
    :param N: Number of positions to consider for regret calculation.
    :return: Updated TSP tour with nodes reinserted.
    """
    while removed_nodes:
        max_regret = -float('inf')
        node_to_insert = None
        insert_position = None

        for node in removed_nodes:
            regret, position = calculate_regret_n(G, tour, node, N)
            if regret > max_regret:
                max_regret = regret
                node_to_insert = node
                insert_position = position

        tour.insert(insert_position, node_to_insert)
        removed_nodes.remove(node_to_insert)
        
    return  tour

def Greedy_Insertion(G, tour, removed_nodes):
        """
        Reinsert the removed nodes into the tour using the Greedy Insertion heuristic.
    
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param removed_nodes: List of nodes to be reinserted.
        :return: Updated TSP tour with nodes reinserted.
        """
        while removed_nodes:
            min_increase = float('inf')
            node_to_insert = None
            best_position = None

            for node in removed_nodes:
                for i in range(1, len(tour)):
                    increase = G[tour[i-1]][node]['length'] + G[node][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
                    if increase < min_increase:
                        min_increase = increase
                        node_to_insert = node
                        best_position = i

            tour.insert(best_position, node_to_insert)
            removed_nodes.remove(node_to_insert)
    
        return  tour

def Best_Insertion(G, tour, removed_nodes):
        """
        Reinsert the removed nodes into the tour using the Best Insertion heuristic.
    
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param removed_nodes: List of nodes to be reinserted.
        :return: Updated TSP tour with nodes reinserted.
        """
        while removed_nodes:
            best_overall_increase = float('inf')
            best_node_to_insert = None
            best_insert_position = None

            # Evaluate each removed node
            for node in removed_nodes:
                for i in range(1, len(tour)):
                    increase = G[tour[i-1]][node]['length'] + G[node][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
                    if increase < best_overall_increase:
                        best_overall_increase = increase
                        best_node_to_insert = node
                        best_insert_position = i

            # Insert the best node at the best position
            tour.insert(best_insert_position, best_node_to_insert)
            removed_nodes.remove(best_node_to_insert)
            
        return tour  

def Cheapest_Insertion(G, tour, removed_nodes):
        """
        Reinsert the removed nodes into the tour using the Cheapest Insertion heuristic.
    
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param removed_nodes: List of nodes to be reinserted.
        :return: Updated TSP tour with nodes reinserted.
        """
        while removed_nodes:
            min_cost_increase = float('inf')
            node_to_insert = None
            best_position = None

            for node in removed_nodes:
                for i in range(1, len(tour)):
                    cost_increase = G[tour[i-1]][node]['length'] + G[node][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
                    if cost_increase < min_cost_increase:
                        min_cost_increase = cost_increase
                        node_to_insert = node
                        best_position = i
            tour.insert(best_position, node_to_insert)
            removed_nodes.remove(node_to_insert)
        return  tour

def Nearest_Insertion(G, tour, removed_nodes):
    
    def find_nearest_node(G, tour, removed_nodes):
        """
        Find the nearest node to the current tour from the list of removed nodes.
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param removed_nodes: List of nodes to be reinserted.
        :return: The nearest node and its distance.
        """
        nearest_node = None
        min_distance = float('inf')
        for node in removed_nodes:
            for tour_node in tour:
                distance = G[node][tour_node]['length']
                if distance < min_distance:
                    min_distance = distance
                    nearest_node = node
        return nearest_node

        """
        Reinsert the removed nodes into the tour using the Nearest Insertion heuristic.
    
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param removed_nodes: List of nodes to be reinserted.
        :return: Updated TSP tour with nodes reinserted.
        """
    while removed_nodes:
        nearest_node = find_nearest_node(G, tour, removed_nodes)
        min_increase = float('inf')
        best_position = None
            
        for i in range(1, len(tour)):
                increase = G[tour[i-1]][nearest_node]['length'] + G[nearest_node][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
                if increase < min_increase:
                    min_increase = increase
                    best_position = i
    
        tour.insert(best_position, nearest_node)
        removed_nodes.remove(nearest_node)
        
    return tour 


def Random_Insertion(G,tour, removed_nodes):
    """
    Reinsert the removed nodes into the tour using the Random Insertion heuristic.
    
    :param tour: Current partial TSP tour.
    :param removed_nodes: List of nodes to be reinserted.
    :return: Updated TSP tour with nodes reinserted at random positions.
    """
    for node in removed_nodes:
        # Randomly select a position to insert the node
        insert_position = random.randint(1, len(tour) - 1)  # Exclude the first and last node if they are the same
        tour.insert(insert_position, node)

    return tour 

def farthest_insertion(G, tour, removed_nodes):
    def find_farthest_node(G, tour, removed_nodes):
        """
        Find the node farthest from the current tour.
        
        :param G: Graph representing the TSP.
        :param tour: Current partial TSP tour.
        :param removed_nodes: List of nodes to be reinserted.
        :return: The farthest node and its distance.
        """
        farthest_node = None
        max_distance = -float('inf')

        for node in removed_nodes:
            for tour_node in tour:
                distance = G[node][tour_node]['length']
                if distance > max_distance:
                    max_distance = distance
                    farthest_node = node

        return farthest_node


    """
    Reinsert the removed nodes into the tour using the Farthest Insertion heuristic.
    
    :param G: Graph representing the TSP.
    :param tour: Current partial TSP tour.
    :param removed_nodes: List of nodes to be reinserted.
    :return: Updated TSP tour with nodes reinserted.
    """
    while removed_nodes:
        farthest_node = find_farthest_node(G, tour, removed_nodes)
        min_increase = float('inf')
        best_position = None

        for i in range(1, len(tour)):
            increase = G[tour[i-1]][farthest_node]['length'] + G[farthest_node][tour[i]]['length'] - G[tour[i-1]][tour[i]]['length']
            if increase < min_increase:
                min_increase = increase
                best_position = i

        tour.insert(best_position, farthest_node)
        removed_nodes.remove(farthest_node)

    return tour



