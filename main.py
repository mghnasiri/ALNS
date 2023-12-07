""" This file use functions or classes from both model.py and output_manager.py.
It acts as the orchestrator, calling the necessary functions from each module and passing data between them. """
# main.py
import networkx as nx
import os
import pandas as pd
from model import create_graph, parse_coordinates, eucl_dist, get_dimension_from_tsp
#from output_manager import visualize_graph
from Initial_solutions import Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion, Cheapest_Insertion


def main():

    # Load the list of dataset
    dataset_paths = ['/Users/Mgh.Nasiri/Documents/1- Academic Documents/3- Laval Universitè/Diriges/Codes/Datasets/TSPLIB/ALL_tsp/eil51.tsp'
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
        print(cities)
       
        initial_tour = Nearest_Neighbor_Heuristic(G, depot)  # Generate an initial tour starting and ending at the depot
        print("Initial TSP Tour:", initial_tour) 
        
        tsp_tour = Christofides_Algorithm(G,depot)
        print("TSP Tour using Christofides' Algorithm:", tsp_tour)
       
        tsp_tour = Minimum_Spanning_Tree_MST_Based_Heuristic(G,depot)
        print("Initial TSP Tour (MST Based Heuristic):", tsp_tour)
        
        tsp_tour = Randomized_Heuristics(G,depot)
        print("TSP Tour (Randomized Heuristic):", tsp_tour)
        
        
        tsp_tour = Farthest_Insertion(G,depot)
        print("TSP Tour (Farthest Insertion):", tsp_tour)
        
        tsp_tour = Cheapest_Insertion(G,depot)
        print("TSP Tour (Cheapest_Insertion):", tsp_tour)
        
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