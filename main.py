""" Contains the core logic of model.
This file  include functions or classes that define your model's behavior, calculations, data processing, etc. """
# model.py
import networkx as nx
import gurobipy as gp
from gurobipy import GRB
import math
import random


# Function to create and initialize the graph


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

def calculate_cost_increase(G, route, new_customer, customer_coords):
    if not route:
        return 0
    last_customer = route[-1]
    return eucl_dist(*customer_coords[last_customer], *customer_coords[new_customer])


import networkx as nx
import math

def eucl_dist(x1, y1, x2, y2):
    return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

def violates_constraints(G, route, new_customer, capacity, max_route_length, demands, customer_coords):
    """
    Check if adding a new customer to the route violates capacity or length constraints.

    :param G: NetworkX graph with edges representing paths between nodes and their lengths.
    :param route: List of customers currently in the route.
    :param new_customer: The customer to be added.
    :param capacity: Maximum capacity of the vehicle.
    :param max_route_length: Maximum allowable length of the route.
    :param demands: Dictionary mapping each customer to their demand.
    :param customer_coords: Dictionary mapping each customer to their coordinates (x, y).
    :return: Boolean indicating if the addition violates constraints.
    """
    # Calculate the total demand with the new customer
    total_demand = sum(demands[customer] for customer in route) + demands[new_customer]
    if total_demand > capacity:
        return True  # Violates capacity constraint

    # Calculate the total length of the route with the new customer
    total_length = 0
    for i in range(len(route) - 1):
        if G.has_edge(route[i], route[i + 1]):
            edge_length = G.edges[route[i], route[i + 1]].get('length', 0)
        else:
            edge_length = eucl_dist(*customer_coords[route[i]], *customer_coords[route[i + 1]])
        total_length += edge_length

    # Add distance from the last customer in the route to the new customer
    if G.has_edge(route[-1], new_customer):
        last_edge_length = G.edges[route[-1], new_customer].get('length', 0)
    else:
        last_edge_length = eucl_dist(*customer_coords[route[-1]], *customer_coords[new_customer])

    total_length += last_edge_length

    return False


def generate_initial_solution(customers, capacity, max_route_length, customer_coords, demands):
    U = set(customers)  # Set of all customers
    routes = []

    while U:
        g = nx.Graph()  # Create a new graph for each route
        seed_customer = random.choice(list(U))
        g.add_node(seed_customer)
        current_route = [seed_customer]
        U.remove(seed_customer)

        while U:
            cost_increase = {c: calculate_cost_increase(g, current_route, c, customer_coords) for c in U}
            c_min = min(cost_increase, key=cost_increase.get)

            if not violates_constraints(g, current_route, c_min, capacity, max_route_length, demands, customer_coords):
                g.add_edge(current_route[-1], c_min)
                current_route.append(c_min)
                U.remove(c_min)
            else:
                break

        routes.append(g)

    return routes



def main():

    # Load the list of dataset
    dataset_paths = ['/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/eil51.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/eil101.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/ch130.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/fl417.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/dsj1000.tsp',
                     #'/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/brd14051.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/d198.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/kroA100.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/kroA150.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/kroB100.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/kroC100.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/kroE100.tsp',
                     '/home/centor.ulaval.ca/ghafomoh/Downloads/ADM-7900/Datasets/TSPLIB/ALL_tsp/berlin52.tsp'
                     ]
    
    for data_path in dataset_paths:
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
        
       
       

""" if __name__ == "__main__":
    main() """