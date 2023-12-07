import random
from Initial_solutions import (
    Nearest_Neighbor_Heuristic, Christofides_Algorithm, 
    Minimum_Spanning_Tree_MST_Based_Heuristic, Randomized_Heuristics, 
    Farthest_Insertion, Cheapest_Insertion, Savings_Algorithm
)
from Removal_Methods import Random_Removal, Worst_Removal, Shaw_Removal
from Insertion_Heuristics import (
    Basic_Insertion, Regret_2_Heuristic, Regret_3_Heuristic, 
    Regret_N_Heuristic, Greedy_Insertion, Best_Insertion, 
    Cheapest_Insertion, Nearest_Insertion, Random_Insertion, farthest_insertion
)



def random_select_heuristics():
    initial_heuristics = [
        Nearest_Neighbor_Heuristic,
        Christofides_Algorithm, 
        Minimum_Spanning_Tree_MST_Based_Heuristic,
        Randomized_Heuristics, 
        Farthest_Insertion,
        Cheapest_Insertion,
        Savings_Algorithm
    ]
    removal_heuristics = [Random_Removal,
                          Worst_Removal,
                          Shaw_Removal
                          ]
    insertion_heuristics = [
        Basic_Insertion,
        Regret_2_Heuristic,
        Regret_3_Heuristic, 
        Regret_N_Heuristic,
        Greedy_Insertion,
        Best_Insertion, 
        Cheapest_Insertion,
        Nearest_Insertion,
        Random_Insertion,
        farthest_insertion
    ]


    
    return (
        random.choice(initial_heuristics),
        random.choice(removal_heuristics),
        random.choice(insertion_heuristics)
    )


