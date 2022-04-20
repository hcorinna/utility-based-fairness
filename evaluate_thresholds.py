import numpy as np
from config_approach import *
import calculate_utilities
import pattern_functions

def to_threshold(r, number_of_thresholds):
    threshold = (1/(number_of_thresholds-1)) * r
    return round(threshold, 2)

def evaluate_model(all_data):
    U_DM = []
    U_DS_A0 = []
    U_DS_A1 = []
    FS = []
    t0 = []
    t1 = []
    for i in range(num_thresholds):
        threshold_0 = to_threshold(i, num_thresholds)
        U_DS_r_A0 = calculate_utilities.U_DS(all_data, 0, threshold_0)
        for j in range(num_thresholds):
            U_DS_A0.append(U_DS_r_A0)
            t0.append(threshold_0)
            threshold_1 = to_threshold(j, num_thresholds)
            t1.append(threshold_1)
            U_DM_r = calculate_utilities.U_DM(all_data, threshold_0, threshold_1)
            U_DM.append(U_DM_r)
            U_DS_r_A1 = calculate_utilities.U_DS(all_data, 1, threshold_1)
            U_DS_A1.append(U_DS_r_A1)
            compare_utilities_function = pattern_functions.get_pattern_function()
            FS_r = compare_utilities_function(U_DS_r_A0, U_DS_r_A1)
            FS.append(FS_r)
    if pattern == 'egalitarianism':
        max_FS = max(FS)
        FS = [max_FS - f for f in FS]
    return U_DM, U_DS_A0, U_DS_A1, FS, t0, t1

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