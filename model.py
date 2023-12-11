""" Contains the core logic of model.
This file  include functions or classes that define your model's behavior, calculations, data processing, etc. """
# model.py
import networkx as nx
import math
from Initial_solutions import Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion, Cheapest_Insertion_Ini, Savings_Algorithm
from Removal_Methods import Random_Removal, Worst_Removal, Shaw_Removal,Related_Removal,Route_Based_Removal
from Insertion_Heuristics import Basic_Insertion,Regret_2_Heuristic,Regret_3_Heuristic, Regret_N_Heuristic,Greedy_Insertion,Best_Insertion, Cheapest_Insertion,Nearest_Insertion,Random_Insertion, farthest_insertion
from Select_Heuristics import random_select_heuristics
from acceptance_functions import simulated_annealing_acceptance,accept_if_better
import random

def eucl_dist(x1, y1, x2, y2):
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2))


def create_graph(data_subset, num_data_points):
    n = len(data_subset) - 1
    # directed graph with a vertex for each city
    G = nx.complete_graph(num_data_points, nx.DiGraph())
    # Add any additional logic for graph initialization
    return G

# Function to parse coordinates (if this is a separate logic in your code)


def parse_coordinates(data_path):
    with open(data_path, 'r') as file:
        lines = file.readlines()
        coord_section = False
        cities = []
        for line in lines:
            if "EOF" in line:
                break
            if coord_section:
                city_info = line.split()
                cities.append((float(city_info[0]), float(
                    city_info[1]), float(city_info[2])))
            if "NODE_COORD_SECTION" in line:
                coord_section = True
    return cities

def get_dimension_from_tsp(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("DIMENSION"):
                # Extract the dimension value
                _, dimension = line.split(':')
                return int(dimension.strip())

def calculate_tour_length(G, tour):
    total_length = 0
    for i in range(len(tour) - 1):
        if tour[i] in G and tour[i + 1] in G[tour[i]]:
            total_length += G[tour[i]][tour[i + 1]].get('length', 0)
        else:
            print(f"Warning: No edge between {tour[i]} and {tour[i + 1]}")
            # Handle the missing edge case or break/return as needed
    return total_length




def iterative_improvement_process(G, start_node, num_iterations,removal_count):
    """
    Apply an iterative improvement process on a TSP solution.
    
    :param G: Graph representing the TSP.
    :param start_node: Starting node for the TSP tour.
    :param num_iterations: Number of iterations for the improvement process.
    :return: Best found TSP tour.
    """
    # Select heuristics
    initial_heuristic, removal_heuristic, insertion_heuristic = random_select_heuristics()
    
    print("Selected Initial Solution Heuristic:", initial_heuristic.__name__)
    print("Selected Removal Heuristic:", removal_heuristic.__name__)
    print("Selected Insertion Heuristic:", insertion_heuristic.__name__)

    # Generate an initial solution
    current_tour = initial_heuristic(G, start_node)
    best_tour = current_tour[:]
    best_tour_length = calculate_tour_length(G, best_tour)

    for _ in range(num_iterations):
        # Apply the removal heuristic
        partial_tour ,removed_nodes = removal_heuristic(G, current_tour,removal_count)

        # Apply the insertion heuristic
        new_tour = insertion_heuristic(G, partial_tour, removed_nodes)

        # Evaluate the new solution
        new_tour_length = calculate_tour_length(G, new_tour)

        
        
        
        # Acceptance criterion (can be replaced with more complex strategies)   
        """acceptance_strategy = 'simulated_annealing'  # or 'accept_if_better'
        if acceptance_strategy == 'accept_if_better':
            accept = accept_if_better(best_tour_length, new_tour_length)
        elif acceptance_strategy == 'simulated_annealing': """
            

        if new_tour_length < best_tour_length:
            best_tour = new_tour[:]
            best_tour_length = new_tour_length

        # Update the current tour for the next iteration
        current_tour = new_tour

    return best_tour


