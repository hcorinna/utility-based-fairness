import numpy as np
from config_approach import *
import calculate_utilities
import pattern_functions
import pandas as pd


def get_thresholds_linear(num_thresholds):
    # thresholds with equal distance to each other, irrespective of the bin sizes
    thresholds = []
    for i in np.linspace(1/num_thresholds, 1, num_thresholds).tolist():
        thresholds.append(i)
    if min(thresholds) > 0:
        thresholds.insert(0,0.0)
    return thresholds



def evaluate_model(all_data):
    U_DM_A0 = {} # decision maker utility group 0
    U_DM_A1 = {} # decision maker utility group 1
    U_DS_A0 = {} # decision subject utility group 0
    U_DS_A1 = {} # decision subject utility group 1

    thresholds = get_thresholds_linear(num_thresholds)

    # calculate DM- and DS-utility for group 0
    for threshold_0 in thresholds:
        U_DS_r_A0 = calculate_utilities.U_DS(all_data, 0, threshold_0)
        U_DS_A0[threshold_0] = U_DS_r_A0
        U_DM_r_A0, n_A0 = calculate_utilities.U_DM(all_data, 0, threshold_0)
        U_DM_A0[threshold_0] = U_DM_r_A0

    # calculate DM- and DS-utility for group 1
    for threshold_1 in thresholds:
        U_DS_r_A1 = calculate_utilities.U_DS(all_data, 1, threshold_1)
        U_DS_A1[threshold_1] = U_DS_r_A1
        U_DM_r_A1, n_A1 = calculate_utilities.U_DM(all_data, 1, threshold_1)
        U_DM_A1[threshold_1] = U_DM_r_A1

    # now calculate utilities and fairness scores for all thresholds combinations
    U_DM_all_thresholds = [] # decision maker utility for all thresholds combinations
    U_DS_A0_all_thresholds = [] # group 0 decision subject utility for all thresholds combinations
    U_DS_A1_all_thresholds = [] # group 1 decision subject utility for all thresholds combinations
    FS = [] # fairness

    for threshold_0 in thresholds:
        for threshold_1 in thresholds:
            U_DM_all_thresholds.append((U_DM_A0[threshold_0] * n_A0 + U_DM_A1[threshold_1] * n_A1) / (n_A0 + n_A1))
            U_DS_A0_all_thresholds.append(U_DS_A0[threshold_0])
            U_DS_A1_all_thresholds.append(U_DS_A1[threshold_1])
            compare_utilities_function = pattern_functions.get_pattern_function()
            FS_r = compare_utilities_function(U_DS_A0[threshold_0], U_DS_A1[threshold_1])
            FS.append(FS_r)

    if pattern == 'egalitarianism':
        max_FS = max(FS)
        FS = [max_FS - f for f in FS]
    return U_DM_all_thresholds, U_DS_A0_all_thresholds, U_DS_A1_all_thresholds, FS

def is_pareto_efficient(points, return_mask = True):
    """
    From: https://stackoverflow.com/questions/32791911/fast-calculation-of-pareto-front-in-python
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :param return_mask: True to return a mask
    :return: An array of indices of pareto-efficient points.
        If return_mask is True, this will be an (n_points, ) boolean array
        Otherwise it will be a (n_efficient_points, ) integer array of indices.
    """
    is_efficient = np.arange(points.shape[0])
    n_points = points.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index<len(points):
        nondominated_point_mask = np.any(points>points[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
        points = points[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1
    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype = bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient