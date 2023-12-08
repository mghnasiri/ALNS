""" This file use functions or classes from both model.py and output_manager.py.
It acts as the orchestrator, calling the necessary functions from each module and passing data between them. """
# main.py
import networkx as nx
import os
import pandas as pd
from model import create_graph, parse_coordinates, eucl_dist, get_dimension_from_tsp,calculate_tour_length,iterative_improvement_process
#from output_manager import visualize_graph
from Initial_solutions import Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion, Cheapest_Insertion_Ini, Savings_Algorithm
from Removal_Methods import Random_Removal, Worst_Removal, Shaw_Removal
from Insertion_Heuristics import Basic_Insertion,Regret_2_Heuristic,Regret_3_Heuristic, Regret_N_Heuristic,Greedy_Insertion,Best_Insertion, Cheapest_Insertion,Nearest_Insertion,Random_Insertion, farthest_insertion
from Select_Heuristics import random_select_heuristics,AdaptiveHeuristicSelector


def main():

    # Load the list of dataset
    dataset_paths = ['/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/eil51.tsp'
                     ]
    for data_path in dataset_paths:
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
        num_iterations = 1000  # Number of iterations for improvement
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
        
        
        #initial_tour = Cheapest_Insertion(G,depot)
        #print("TSP Tour (Cheapest_Insertion):", initial_tour)
        
        #initial_tour = Savings_Algorithm(G,depot)
        #print("TSP Tour (Savings Algorithm):", initial_tour)
             
        
        
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
        
        # Initialize the adaptive heuristic selector
        selector = AdaptiveHeuristicSelector(
            AdaptiveHeuristicSelector.initial_heuristics,
            AdaptiveHeuristicSelector.removal_heuristics,
            AdaptiveHeuristicSelector.insertion_heuristics
        )
        

        
        for i in range(num_iterations):

                # Select and apply the initial solution heuristic
            initial_heuristic = selector.select_heuristic('initial')
            tour = initial_heuristic(G, depot)

            # Select and apply the removal heuristic
            removal_heuristic = selector.select_heuristic('removal')
            tour, removed_nodes = removal_heuristic(G, tour, removal_count)

            # Select and apply the insertion heuristic
            insertion_heuristic = selector.select_heuristic('insertion')
            tour = insertion_heuristic(G, tour, removed_nodes)  # Pass removed_nodes here
            
            current_length = calculate_tour_length(G, tour)
            improvement = current_length < best_length
            if improvement:
                best_tour, best_length = tour, current_length
                
            # Update heuristic scores using the instance
            selector.update_heuristic_score(initial_heuristic, improvement, 'initial')
            selector.update_heuristic_score(removal_heuristic, improvement, 'removal')
            selector.update_heuristic_score(insertion_heuristic, improvement, 'insertion')

            # Print information about the iteration (optional)
            print(f"Iteration {i + 1}: Length of Tour = {current_length}")
                        # Print the best tour and its length
            print("Best Tour:", best_tour)
            print("Length of Best Tour:", best_length)
        







        
        """
        model = solve_TSP_MTZ_problem(G, dem_points, depot, k)
        
        # Assuming model is the returned Gurobi model from solve_TSP_MTZ_problem
        x_vars = model.getVars()
        x = {e: x_var for e, x_var in zip(G.edges, x_vars)}
        results = get_optimization_results(model)
        
        output_file_path = f"/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/{dataset_name_with_extension}.png"
        # If graph visualization is needed
           visualize_graph(G, depot, nx, x, my_pos, results,
                        dataset_name_with_extension, output_file_path)
        """




if __name__ == "__main__":
    main()