import pandas as pd
import numpy as np


def create_award_index(nr_nominations, nr_wins):
    """
    Function creating an index for the awards 
    nr_nominations: column of a panda series with integers or floats indicating the times of nominations
    nr_wins: column of a panda series with integers or floats indicationg the times of wins 

    Output: award index in list form according to the actors nominations and wins for acting awards.

    Creating the award index:
    0 points if never nominated, 
    1 point if at least once nominated
    2 points if at least once won
    3 points if more than once won
    """
    award_indices = []
    for nominations, wins in zip(nr_nominations, nr_wins):
        if wins > 1:
            award_index = 3
        elif wins == 1:
            award_index = 2
        elif nominations >= 0:
            award_index = 1
        else:
            award_index = 0 
        award_indices.append(award_index)
    return award_indices