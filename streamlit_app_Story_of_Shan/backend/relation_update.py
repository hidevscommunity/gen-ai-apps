import numpy as np

def calculate_rank_difference(base_rank, k=1, positive = False):
    # Calculate the inverted difference using the logistic function
    rank_difference = np.abs(base_rank - 0.5)
    rank_difference = 1 - (1 / (1 + np.exp(-k * rank_difference)))
    rank_difference = rank_difference*0.05
    
    return max(0,min(positive + positive*rank_difference,1))
