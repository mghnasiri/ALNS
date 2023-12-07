""" Contains the core logic of model.
This file  include functions or classes that define your model's behavior, calculations, data processing, etc. """
# model.py
import networkx as nx
import math

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