from model import create_graph, parse_coordinates, eucl_dist, get_dimension_from_tsp,calculate_tour_length,iterative_improvement_process
#from output_manager import visualize_graph
from Initial_solutions import Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion, Cheapest_Insertion_Ini, Savings_Algorithm,basic_greedy_heuristic,regret_2_heuristic,regret_3_heuristic,regret_n_heuristic
from Removal_Methods import Random_Removal, Worst_Removal, Shaw_Removal,Related_Removal,Route_Based_Removal
from Insertion_Heuristics import Basic_Insertion,Regret_2_Heuristic,Regret_3_Heuristic, Regret_N_Heuristic,Greedy_Insertion,Best_Insertion, Cheapest_Insertion,Nearest_Insertion,Random_Insertion, farthest_insertion
from Select_Heuristics import random_select_heuristics,AdaptiveHeuristicSelector
from output_manager import visualize_graph,plot_length_improvement,plot_heuristic_weights
import time
import networkx as nx
import os
import pandas as pd
import logging

def test_heuristic(heuristic, problem_instance, evaluate_solution, *args, **kwargs):
    """
    Test a heuristic on a given problem instance.

    Args:
    heuristic (function): The heuristic function to test.
    problem_instance: The problem instance to apply the heuristic on.
    evaluate_solution (function): Function to evaluate the quality of the solution.
    *args, **kwargs: Additional arguments for the heuristic function.

    Returns:
    dict: A dictionary containing the solution quality, runtime, and success status.
    """
    start_time = time.time()
    try:
        solution = heuristic(problem_instance, *args, **kwargs)
        runtime = time.time() - start_time
        quality = evaluate_solution(solution)
        success = True
    except Exception as e:
        runtime = time.time() - start_time
        quality = None
        success = False
        print(f"Testing failed: {e}")

    return {
        "quality": quality,
        "runtime": runtime,
        "success": success
    }

for heuristic in [Nearest_Neighbor_Heuristic, Christofides_Algorithm,
                               Minimum_Spanning_Tree_MST_Based_Heuristic, Randomized_Heuristics,
                               Farthest_Insertion, Cheapest_Insertion_Ini, Savings_Algorithm,
                               basic_greedy_heuristic, regret_2_heuristic, regret_3_heuristic,
                               regret_n_heuristic]:  # Include all your heuristics
    dataset_paths = [#'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/eil51.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/eil101.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/ch130.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/fl417.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/dsj1000.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/brd14051.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/First Python Code/eil51.tsp'
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/eil51.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/eil101.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/ch130.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/fl417.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/dsj1000.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/brd14051.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/d198.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroA100.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroA150.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroB100.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroC100.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroE100.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/berlin52.tsp'
                     ]
    for data_path in dataset_paths:
         # Configure logging
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)        
        
        logging.basicConfig(filename=os.path.splitext(os.path.basename(data_path))[0], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f'Processing dataset: {data_path}')
            
        # data_path = '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/eil51.tsp'
        dataset_name_with_extension = os.path.basename(data_path)
        data = pd.read_csv(data_path)
        # Number of data points you want to use (including depot)
        num_data_points = get_dimension_from_tsp(
            data_path)  # Adjust this value as needed
        # Extract a subset based on the desired number of data points
        data_subset = data.head(num_data_points)
        n = len(data_subset)-1
        Q = 200
        k = 1                       # number of vehicles
        depot = 0
        dem_points = list(range(1, n+1))  # nodes 1, 2, ..., 20
        removal_count = 1  # Number of nodes to remove
        num_iterations = 10  # Number of iterations for improvement
        best_tour = None
        best_length = float('inf')
        start_time = time.time()


        G = create_graph(data_subset, num_data_points)
        cities = parse_coordinates(data_path)
        my_pos = {point[0]-1: (point[1], point[2])
                for point in cities}  # pos[i] = (x_i, y_i)«
        for i, j in G.edges:
            (x1, y1) = my_pos[i]
            (x2, y2) = my_pos[j]
            G.edges[i, j]['length'] = eucl_dist(x1, y1, x2, y2)
        cities = parse_coordinates(data_path)
        
        def evaluate_solution(solution, graph):
            """
            Evaluate the quality of a solution.

            Args:
            solution (list): The solution to evaluate, typically a list of node indices.
            graph: The graph representing your problem, with distances or costs between nodes.

            Returns:
            float: The quality of the solution, lower values are better.
            """
            total_distance = 0
            for i in range(len(solution) - 1):
                total_distance += graph.get_edge_data(solution[i], solution[i+1])['length']
            return total_distance

    
    
        result = test_heuristic(heuristic, G, lambda solution: evaluate_solution(solution, G))

        

            

