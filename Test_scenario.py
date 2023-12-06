from model import eucl_dist
from main import generate_initial_solution

customer_coords = {
    'A': (0, 0),
    'B': (3, 4),
    'C': (7, 6),
    'D': (2, 8),
    'E': (5, 5)
}

demands = {
    'A': 10,
    'B': 15,
    'C': 10,
    'D': 20,
    'E': 10
}

capacity = 40  # Vehicle capacity
max_route_length = 100  # Maximum allowable route length

initial_solution = generate_initial_solution(
    list(customer_coords.keys()),
    capacity,
    max_route_length,
    customer_coords,
    demands
)

for i, route in enumerate(initial_solution, start=1):
    route_demand = sum(demands[node] for node in route.nodes)
    route_length = sum(eucl_dist(*customer_coords[edge[0]], *customer_coords[edge[1]]) for edge in route.edges)

    print(f"Route {i}: Nodes = {list(route.nodes)}, Total Demand = {route_demand}, Total Length = {route_length}")
    assert route_demand <= capacity, f"Route {i} violates capacity constraint."
    assert route_length <= max_route_length, f"Route {i} violates length constraint."
