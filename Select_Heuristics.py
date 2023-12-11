import random
from Initial_solutions import Nearest_Neighbor_Heuristic, Christofides_Algorithm,Minimum_Spanning_Tree_MST_Based_Heuristic,Randomized_Heuristics,Farthest_Insertion_INI, Cheapest_Insertion_Ini, Savings_Algorithm,basic_greedy_heuristic,regret_2_heuristic_ini,regret_3_heuristic_ini
from Removal_Methods import Random_Removal, Worst_Removal, Shaw_Removal,Related_Removal,Route_Based_Removal
from Insertion_Heuristics import Basic_Insertion,Regret_2_Heuristic,Regret_3_Heuristic, Regret_N_Heuristic,Greedy_Insertion,Best_Insertion, Cheapest_Insertion,Nearest_Insertion,Random_Insertion, farthest_insertion



def random_select_heuristics():
    initial_heuristics = [
        Nearest_Neighbor_Heuristic,
        Christofides_Algorithm, 
        Minimum_Spanning_Tree_MST_Based_Heuristic,
        Randomized_Heuristics, 
        Farthest_Insertion_INI,
        Cheapest_Insertion_Ini,
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



class AdaptiveHeuristicSelector:
    
    initial_heuristics = [
        Nearest_Neighbor_Heuristic,
        Christofides_Algorithm, 
        Minimum_Spanning_Tree_MST_Based_Heuristic,
        Randomized_Heuristics, 
        Farthest_Insertion_INI,
        Cheapest_Insertion_Ini,
        #Savings_Algorithm
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
    
    
    def __init__(self, initial_heuristics, removal_heuristics, insertion_heuristics, alpha=0.1):
            self.initial_heuristics = initial_heuristics
            self.removal_heuristics = removal_heuristics
            self.insertion_heuristics = insertion_heuristics
            self.initial_solution_scores = {heuristic: 1 for heuristic in self.initial_heuristics}
            self.removal_method_scores = {heuristic: 1 for heuristic in self.removal_heuristics}
            self.insertion_heuristic_scores = {heuristic: 1 for heuristic in self.insertion_heuristics}
            self.alpha = alpha

    def update_heuristic_score(self, heuristic, success, category):
        """
        Update the score of a heuristic based on its success.

        :param heuristic: The heuristic function to update.
        :param success: Boolean indicating if the heuristic was successful.
        :param category: Category of the heuristic ('initial', 'removal', 'insertion').
        """
        score_dict = self._get_score_dict(category)
        if success:
            score_dict[heuristic] += self.alpha
        else:
            score_dict[heuristic] = max(score_dict[heuristic] - self.alpha, 0.1)  # Prevent score from going below 0.1

    def select_heuristic(self, category):
        """
        Select a heuristic based on weighted random choice.

        :param category: Category of the heuristic ('initial', 'removal', 'insertion').
        :return: Selected heuristic.
        """
        score_dict = self._get_score_dict(category)
        return self._weighted_random_choice(score_dict)

    def _get_score_dict(self, category):
        if category == 'initial':
            return self.initial_solution_scores
        elif category == 'removal':
            return self.removal_method_scores
        elif category == 'insertion':
            return self.insertion_heuristic_scores
        else:
            raise ValueError("Invalid category")

    def _weighted_random_choice(self, score_dict):
        total_score = sum(score_dict.values())
        r = random.uniform(0, total_score)
        upto = 0
        for heuristic, score in score_dict.items():
            if upto + score >= r:
                return heuristic
            upto += score

