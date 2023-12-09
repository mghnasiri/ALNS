import math
import random

def simulated_annealing_acceptance(current_solution, new_solution, temperature):
    if new_solution.quality >= current_solution.quality:
        return True
    else:
        probability = math.exp((new_solution.quality - current_solution.quality) / temperature)
        return random.random() < probability


def accept_if_better(current_solution, new_solution):
    return new_solution.quality >= current_solution.quality
