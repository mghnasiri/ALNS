""" This file use functions or classes from both model.py and output_manager.py.
It acts as the orchestrator, calling the necessary functions from each module and passing data between them. """
# main.py
import networkx as nx
import os
import pandas as pd
import logging
import time

from model import create_graph, parse_coordinates, eucl_dist, get_dimension_from_tsp,calculate_tour_length,iterative_improvement_process
#from output_manager import visualize_graph
from Initial_solutions import Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion, Cheapest_Insertion_Ini, Savings_Algorithm,basic_greedy_heuristic,regret_2_heuristic,regret_3_heuristic
from Removal_Methods import Random_Removal, Worst_Removal, Shaw_Removal,Related_Removal,Route_Based_Removal
from Insertion_Heuristics import Basic_Insertion,Regret_2_Heuristic,Regret_3_Heuristic, Regret_N_Heuristic,Greedy_Insertion,Best_Insertion, Cheapest_Insertion,Nearest_Insertion,Random_Insertion, farthest_insertion
from Select_Heuristics import random_select_heuristics,AdaptiveHeuristicSelector
from output_manager import visualize_graph,plot_length_improvement,plot_heuristic_weights



def main():
     
    results = []
    

    # Load the list of dataset
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
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/fl417.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/dsj1000.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/brd14051.tsp',
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


        G = create_graph(data_subset, num_data_points)
        cities = parse_coordinates(data_path)
        my_pos = {point[0]-1: (point[1], point[2])
                  for point in cities}  # pos[i] = (x_i, y_i)«
        for i, j in G.edges:
            (x1, y1) = my_pos[i]
            (x2, y2) = my_pos[j]
            G.edges[i, j]['length'] = eucl_dist(x1, y1, x2, y2)
        cities = parse_coordinates(data_path)
  
        # Assuming you want to print this based on your original script
        #print(cities)
        # List your heuristics
        best_lengths = []
        current_lengths = []
        initial_heuristics = [Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion, Cheapest_Insertion_Ini, Savings_Algorithm,basic_greedy_heuristic,regret_2_heuristic]
        removal_heuristics = [Random_Removal, Worst_Removal, Shaw_Removal,Related_Removal,Route_Based_Removal]
        insertion_heuristics = [Basic_Insertion,Regret_2_Heuristic,Regret_3_Heuristic, Regret_N_Heuristic,Greedy_Insertion,Best_Insertion, Cheapest_Insertion,Nearest_Insertion,Random_Insertion, farthest_insertion]        
        # Loop through all combinations
        for initial in initial_heuristics:
            for removal in removal_heuristics:
                for insertion in insertion_heuristics:                    
                    for i in range(10):
                        start_time = time.time()
                        total_runtime = 0
                        total_tour_length = 0
                        num_iterations = 100
                        initial_tour = initial(G,depot)
                        print(f"Initial Tour: {initial} {initial_tour}")
                        logging.info(f'{initial} - Initial Tour: {initial_tour}')
                        best_solution_cost = calculate_tour_length(G, initial_tour)
                        print(f"best_solution_cost: {initial} {best_solution_cost}")
                        logging.info(f'{initial} - Initial Tour: {best_solution_cost}')
                        
                        for j in range(num_iterations):
                            print(f"--- Iteration {j + 1} ---")
                            logging.info(f"--- Iteration {j + 1} ---")
                            # Removal
                            new_tour, removed_nodes = removal(G, initial_tour, removal_count)
                            print(f"{removal} - Tour after Removal: {new_tour}, Removed Nodes: {removed_nodes}")
                            logging.info(f'{removal} - Tour after Removal: {new_tour}, Removed Nodes: {removed_nodes}')
                            
                            # Select and apply the insertion heuristic
                            new_tour = insertion(G, new_tour, removed_nodes)  # Pass removed_nodes here
                            print(f"{insertion} -Tour after Insertion: {new_tour}")
                            logging.info(f'{insertion} -Tour after Insertion: {new_tour}')
                            current_length = calculate_tour_length(G, new_tour)
                            print(f"{insertion} - Length of Current Tour: {current_length}")
                            logging.info(f'{insertion} - Length of Current Tour: {current_length}')
                            # Check for improvement
                            if current_length < best_length:
                                best_length = current_length
                                best_tour = new_tour
                                print(f"New Best Tour Found: {best_tour}, Length: {best_length}")
                                logging.info(f'New Best Tour Found: {best_tour}, Length: {best_length}')
                            else:
                                print("No improvement in this iteration.")
                                logging.info(f'No improvement in this iteration.')
                            print()  # Blank line for better readability
                        
                        logging.info(f'')
                        # Print information about the iteration (optional)
                        print(f"Iteration {j + 1}: Length of Tour = {current_length}")
                        logging.info(f'Iteration {j + 1}: Length of Tour = {current_length}')

                                    # Print the best tour and its length
                        print("Best Tour:", best_tour)
                        logging.info(f'Best Tour: = {best_tour}')
                        best_lengths.append(best_length)
                        current_lengths.append(current_length)
                                
                        end_time = time.time()        
                        best_tour_length = calculate_tour_length(G, initial_tour)
                        logging.info(f'Length of Best Tour: = {best_tour_length}')
                        runtime = end_time - start_time  # Calculate runtime
                        logging.info(f'Length of runtime: = {runtime}')
                        total_runtime += runtime
                        total_tour_length += best_tour_length
                    average_runtime = total_runtime / 10
                    average_tour_length = total_tour_length / 10
                    logging.info(f"Average Runtime: {average_runtime:.4f} seconds")
                    logging.info(f"Average Best Tour Length: {average_tour_length}")

                
                            

                    
if __name__ == "__main__":
    main()