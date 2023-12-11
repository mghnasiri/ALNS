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
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/eil51.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/eil101.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/ch130.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/fl417.tsp',
                     '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/dsj1000.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/brd14051.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/d198.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroA100.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroA150.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroB100.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroC100.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/kroE100.tsp',
                     #'/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/berlin52.tsp'
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
        total_runtime = 0
        total_tour_length = 0
        num_iterations = 100
        # Assuming you want to print this based on your original script
        #print(cities)
        for i in range(100):
            start_time = time.time()
            #initial_tour = Nearest_Neighbor_Heuristic(G, depot)  # Generate an initial tour starting and ending at the depot
            #print("Initial TSP Tour:", initial_tour) 
            
            #initial_tour = Christofides_Algorithm(G,depot)
            #print("TSP Tour using Christofides' Algorithm:", initial_tour)
        
            #initial_tour = Minimum_Spanning_Tree_MST_Based_Heuristic(G,depot)
            #print("Initial TSP Tour (MST Based Heuristic):", initial_tour)
            
            #initial_tour = Randomized_Heuristics(G,depot)
            #print("TSP Tour (Randomized Heuristic):", initial_tour)
            
            
            #initial_tour = Farthest_Insertion(G,depot)
            #print("TSP Tour (Farthest Insertion):", initial_tour)
            
            
            #initial_tour = Cheapest_Insertion_Ini(G,depot)
            #print("TSP Tour (Cheapest_Insertion_Ini):", initial_tour)
            
            initial_tour = Savings_Algorithm(G,depot)
            print("TSP Tour (Savings Algorithm):", initial_tour)

            #initial_tour = basic_greedy_heuristic(G,depot)
            #print("TSP Tour (basic_greedy_heuristic):", initial_tour)
            
            #initial_tour = regret_2_heuristic(G,depot)
            #print("TSP Tour (regret_2_heuristic):", initial_tour)
            
            #initial_tour = regret_3_heuristic(G,depot)
            #print("TSP Tour (regret_3_heuristic):", initial_tour)
                        
            
            #initial_tour = regret_n_heuristic(G,depot,5)
            #print("TSP Tour (regret_n_heuristic):", initial_tour)
            
            end_time = time.time()        
            best_tour_length = calculate_tour_length(G, initial_tour)
            
            logging.info(f'Length of Best Tour: = {best_tour_length}')
            runtime = end_time - start_time  # Calculate runtime
            logging.info(f'Length of runtime: = {runtime}')
            total_runtime += runtime
            total_tour_length += best_tour_length
        
        average_runtime = total_runtime / num_iterations
        average_tour_length = total_tour_length / num_iterations
        logging.info(f"Average Runtime: {average_runtime:.4f} seconds")
        logging.info(f"Average Best Tour Length: {average_tour_length}")




             
        
        #new_tour, removed_nodes = Random_Removal(G, initial_tour, removal_count)
        #print("New Tour after Random Removal:", new_tour)
        #print("Removed Nodes:", removed_nodes)
        
        #new_tour, removed_nodes = Worst_Removal(G, initial_tour, removal_count)
        #print("New Tour after worst removal:", new_tour)
        #print("Removed Nodes:", removed_nodes)
        
        #new_tour, removed_nodes = Shaw_Removal(G, initial_tour, removal_count)
        #print("New Tour after Shaw_Removal:", new_tour)
        #print("Removed Nodes:", removed_nodes)
        
        #new_tour, removed_nodes = Related_Removal(G, initial_tour, removal_count)
        #print("New Tour after Related_Removal:", new_tour)
        #print("Removed Nodes:", removed_nodes)
        
        #new_tour, removed_nodes = Route_Based_Removal(G, initial_tour, removal_count)
        #print("New Tour after Route_Based_Removal:", new_tour)
        #print("Removed Nodes:", removed_nodes)
        
        
        #updated_tour = Basic_Insertion(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        
        #updated_tour = Regret_2_Heuristic(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        
        #updated_tour = Regret_3_Heuristic(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #updated_tour = Regret_N_Heuristic(G, new_tour, removed_nodes,2)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #updated_tour = Greedy_Insertion(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #updated_tour = Best_Insertion(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #updated_tour = Cheapest_Insertion(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #updated_tour = Nearest_Insertion(G, new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        
        #updated_tour = Random_Insertion(G,new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #updated_tour = farthest_insertion(G,new_tour, removed_nodes)
        #print("Updated TSP Tour after Reinserting Removed Nodes:", updated_tour)
        
        #best_tour = iterative_improvement_process(G, depot, num_iterations,removal_count)
        #best_tour_length = calculate_tour_length(G, best_tour)

        #print("Best TSP Tour:", best_tour)
        #print("Total Length of Best Tour:", best_tour_length)
        """ 
        # Initialize the adaptive heuristic selector
        selector = AdaptiveHeuristicSelector(
            AdaptiveHeuristicSelector.initial_heuristics,
            AdaptiveHeuristicSelector.removal_heuristics,
            AdaptiveHeuristicSelector.insertion_heuristics
        )
        
        # Initialize lists to track lengths
        best_lengths = []
        current_lengths = []
        # Initialize dictionaries to track weights
        removal_weights_dict = {'Random_Removal': [], 'Worst_Removal': [], 'Shaw_Removal': [], 'Related_Removal': [], 'Route_Based_Removal': []}
        insertion_weights_dict = {'Basic_Insertion': [], 'Regret_2_Heuristic': [], 'Regret_3_Heuristic':[],'Regret_N_Heuristic':[],'Greedy_Insertion':[],'Best_Insertion':[],'Cheapest_Insertion':[],'Savings_Algorithm':[],'Nearest_Insertion' :[],'Random_Insertion' :[],'farthest_insertion' :[]}
        Initial_weights_dict = {'Nearest_Neighbor_Heuristic': [], 'Christofides_Algorithm': [], 'Minimum_Spanning_Tree_MST_Based_Heuristic':[],'Randomized_Heuristics':[],'Farthest_Insertion':[],'Cheapest_Insertion_Ini':[],'Savings_Algorithm':[],'basic_greedy_heuristic':[],'regret_2_heuristic':[],'regret_3_heuristic' :[],'regret_n_heuristic' :[]}



        for i in range(num_iterations):
            print(f"--- Iteration {i + 1} ---")


                # Select and apply the initial solution heuristic
            initial_heuristic = selector.select_heuristic('initial')
            tour = initial_heuristic(G, depot)
            print(f"Initial Tour: {tour}")
            logging.info(f'Initial Tour: {tour}')



            # Select and apply the removal heuristic
            removal_heuristic = selector.select_heuristic('removal')
            tour, removed_nodes = removal_heuristic(G, tour, removal_count)
            print(f"Tour after Removal: {tour}, Removed Nodes: {removed_nodes}")
            logging.info(f'Tour after Removal: {tour}, Removed Nodes: {removed_nodes}')



            # Select and apply the insertion heuristic
            insertion_heuristic = selector.select_heuristic('insertion')
            tour = insertion_heuristic(G, tour, removed_nodes)  # Pass removed_nodes here
            print(f"Tour after Insertion: {tour}")
            logging.info(f'Tour after Insertion: {tour}')


            
            
            current_length = calculate_tour_length(G, tour)
            print(f"Length of Current Tour: {current_length}")
            logging.info(f'Length of Current Tour: {current_length}')


            # Check for improvement
            if current_length < best_length:
                best_length = current_length
                best_tour = tour
                print(f"New Best Tour Found: {best_tour}, Length: {best_length}")
                logging.info(f'New Best Tour Found: {best_tour}, Length: {best_length}')


            else:
                print("No improvement in this iteration.")
                logging.info(f'No improvement in this iteration.')

                
                # Update scores
            success = current_length < best_length
            selector.update_heuristic_score(initial_heuristic, success, 'initial')
            print(f"Updated score for {initial_heuristic.__name__}: {selector.initial_solution_scores[initial_heuristic]}")
            logging.info(f'Updated score for {initial_heuristic.__name__}: {selector.initial_solution_scores[initial_heuristic]}')


            selector.update_heuristic_score(removal_heuristic, success, 'removal')
            print(f"Updated score for {removal_heuristic.__name__}: {selector.removal_method_scores[removal_heuristic]}")
            logging.info(f'Updated score for {removal_heuristic.__name__}: {selector.removal_method_scores[removal_heuristic]}')


            selector.update_heuristic_score(insertion_heuristic, success, 'insertion')
            print(f"Updated score for {insertion_heuristic.__name__}: {selector.insertion_heuristic_scores[insertion_heuristic]}")
            logging.info(f'Updated score for {insertion_heuristic.__name__}: {selector.insertion_heuristic_scores[insertion_heuristic]}')



            print()  # Blank line for better readability
            logging.info(f'')


            # Print information about the iteration (optional)
            print(f"Iteration {i + 1}: Length of Tour = {current_length}")
            logging.info(f'Iteration {i + 1}: Length of Tour = {current_length}')

                        # Print the best tour and its length
            print("Best Tour:", best_tour)
            logging.info(f'Best Tour: = {best_tour}')
            best_lengths.append(best_length)
            current_lengths.append(current_length)
            # Update weights in dictionaries
            #Initial_weights_dict[initial_heuristic.__name__].append(selector.initial_solution_scores[initial_heuristic])
            #removal_weights_dict[removal_heuristic.__name__].append(selector.removal_method_scores[removal_heuristic])
            #insertion_weights_dict[insertion_heuristic.__name__].append(selector.insertion_heuristic_scores[insertion_heuristic])
            
            # ... ALNS algorithm steps ...
            # Assuming 'removal_heuristic' is the heuristic used in this iteration
            current_removal_heuristic = removal_heuristic.__name__

            # Update weights for all removal heuristics
            for heuristic_name in removal_weights_dict.keys():
                if heuristic_name == current_removal_heuristic:
                    # Heuristic was used in this iteration, append its current weight
                    removal_weights_dict[heuristic_name].append(selector.removal_method_scores[removal_heuristic])
                else:
                    # Heuristic was not used, append the last known weight
                    if removal_weights_dict[heuristic_name]:  # Check if the list is not empty
                        removal_weights_dict[heuristic_name].append(removal_weights_dict[heuristic_name][-1])
                    else:
                        # If the list is empty (first iteration), append an initial weight
                        removal_weights_dict[heuristic_name].append(1)
            
            # Assuming 'insertion_heuristic' is the heuristic used in this iteration for insertion
            current_insertion_heuristic = insertion_heuristic.__name__

            # Update weights for all insertion heuristics
            for heuristic_name in insertion_weights_dict.keys():
                if heuristic_name == current_insertion_heuristic:
                    # Heuristic was used in this iteration, append its current weight
                    insertion_weights_dict[heuristic_name].append(selector.insertion_heuristic_scores[insertion_heuristic])
                else:
                    # Heuristic was not used, append the last known weight
                    if insertion_weights_dict[heuristic_name]:  # Check if the list is not empty
                        insertion_weights_dict[heuristic_name].append(insertion_weights_dict[heuristic_name][-1])
                    else:
                        # If the list is empty (first iteration), append an initial weight
                        insertion_weights_dict[heuristic_name].append(1)
            
            
            # Assuming 'initial_heuristic' is the heuristic used in this iteration
            current_initial_heuristic = initial_heuristic.__name__
            # Update weights for all initial heuristics
            for heuristic_name in Initial_weights_dict.keys():
                if heuristic_name == current_initial_heuristic:
                    # Heuristic was used in this iteration, append its current weight
                    Initial_weights_dict[heuristic_name].append(selector.initial_solution_scores[initial_heuristic])
                else:
                    # Heuristic was not used, append the last known weight
                    if Initial_weights_dict[heuristic_name]:  # Check if the list is not empty
                        Initial_weights_dict[heuristic_name].append(Initial_weights_dict[heuristic_name][-1])
                    else:
                        # If the list is empty (first iteration), append an initial weight
                        Initial_weights_dict[heuristic_name].append(1)





            print("Length of Best Tour:", best_length)
            logging.info(f'Length of Best Tour: = {best_length}')
            # If graph visualization is needed
        
        output_file_path = '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/ALNS/ALNS2/ALNS/' + dataset_name_with_extension + '.png'
        output_file_path2 = '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/ALNS/ALNS2/ALNS/' + dataset_name_with_extension + 'plot_length_improvement.png'
        #output_file_path = '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/ALNS/ALNS/' + dataset_name_with_extension + '.png'
        #output_file_path2 = '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/ALNS/ALNS/' + dataset_name_with_extension + 'plot_length_improvement.png'

        output_file_path3 = '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/ALNS/ALNS2/ALNS/' + dataset_name_with_extension + 'Weights Progression - Removal Heuristics.png'
        output_file_path4 = '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/ALNS/ALNS2/ALNS/' + dataset_name_with_extension + 'Weights Progression - Insertion Heuristics.png'
        output_file_path5 = '/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/ALNS/ALNS2/ALNS/' + dataset_name_with_extension + 'Weights Progression - Initial Heuristics.png'


        visualize_graph(G, depot,nx, best_tour,my_pos, dataset_name_with_extension, output_file_path)
        plot_length_improvement(best_lengths, current_lengths, output_file_path2,dataset_name_with_extension,dpi=300,title='My Algorithm Length Improvement')
        plot_heuristic_weights(num_iterations, Initial_weights_dict,output_file_path5,dpi=300, title='Weights Progression - Initial Heuristics')
        plot_heuristic_weights(num_iterations, removal_weights_dict, output_file_path3,dpi=300, title='Weights Progression - Removal Heuristics')
        plot_heuristic_weights(num_iterations, insertion_weights_dict,output_file_path4,dpi=300, title='Weights Progression - Insertion Heuristics')
        # After the ALNS loop
        for heuristic, weights in removal_weights_dict.items():
            print(f"{heuristic}: Length = {len(weights)}, Data = {weights[:10]}")  # Print the first 10 weights
 """
        end_time = time.time()
       


        

if __name__ == "__main__":
    main()