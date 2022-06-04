import numpy as np
from config_approach import *
import pattern_functions
import pandas as pd
import config_data


def get_thresholds_linear(num_thresholds, p=None):
    # thresholds with equal distance to each other, irrespective of the bin sizes
    thresholds = []
    for i in np.linspace(1/num_thresholds, 1, num_thresholds).tolist():
        thresholds.append(i)
    if min(thresholds) > 0:
        thresholds.insert(0, 0.0)
    return thresholds


def get_upper_and_lower_bound_thresholds(num_thresholds, p):
    # get thresholds with equal distance to each other, irrespective of the bin sizes
    # every "threshold" yields two decision rules: one upper- and one lower-bound threshold.
    # for example, for thresholds=0.1, a lower-bound threshold means that all individuals with a p>0.1 are assigned D=1. An upper-bound threshold means that all individuals with a p<0.1 are assigned D=1.
    thresholds = []
    for i in np.linspace(1/num_thresholds, 1, num_thresholds).tolist():
        thresholds.append((0, i))
    for i in np.linspace(1/num_thresholds, 1-1/num_thresholds, num_thresholds-1).tolist():
        thresholds.append((i, 1.0))
    return thresholds


def get_thresholds_quantile_based(num_thresholds, p):
    # get thresholds with equally sized buckets (i.e., depending on the score distribution)
    results, bin_edges = pd.qcut(
        p, q=num_thresholds, retbins=True, duplicates="drop")
    thresholds = list(bin_edges)
    if min(p) < 0.1 and min(p) >= 0:
        thresholds.insert(0, 0.0)
    if max(p) > 0.9 and max(p) <= 1:
        thresholds.append(1.0)
    return thresholds


def get_upper_and_lower_bound_thresholds_quantile_based(num_thresholds, p):
    # get thresholds with equally sized buckets (i.e., depending on the score distribution)
    # every "threshold" yields two decision rules: one upper- and one lower-bound threshold.
    # for example, for thresholds=0.1, a lower-bound threshold means that all individuals with a p>0.1 are assigned D=1. An upper-bound threshold means that all individuals with a p<0.1 are assigned D=1.
    results, bin_edges = pd.qcut(
        p, q=num_thresholds, retbins=True, duplicates="drop")
    thresholds = list(bin_edges)
    if min(p) < 0.1 and min(p) >= 0:
        thresholds.insert(0, 0.0)
    if max(p) > 0.9 and max(p) <= 1:
        thresholds.append(1.0)
    threshold_tuples = []
    minimum, maximum = min(thresholds), max(thresholds)
    for t in thresholds:
        new_tuple = (minimum, t)
        if minimum != t and new_tuple not in threshold_tuples:
            threshold_tuples.append(new_tuple)
    for t in thresholds:
        new_tuple = (t, maximum)
        if maximum != t and new_tuple not in threshold_tuples:
            threshold_tuples.append(new_tuple)
    return threshold_tuples


def calculate_utilities(data, A_value, threshold):
    if decision_rules in ['linear-lower', 'quantile-based-lower']:
        data['D'] = data['p'] >= threshold
    elif decision_rules in ['linear-upper-and-lower', 'quantile-based-upper-and-lower']:
        data['D'] = data['p'].between(threshold[0], threshold[1])

    expected_utility_DM = 0
    expected_utility_DS = 0
    counter_DM = 0
    counter_DS = 0
    for index, decision_subject in data.iterrows():
        if decision_subject[A] == A_value:
            y_i = decision_subject['Y']
            p_i = decision_subject['p']
            d_i = decision_subject['D']
            # calculate the decision maker utility
            u_DM = v_11 * d_i * y_i + v_10 * d_i * \
                (1-y_i) + v_01 * (1-d_i) * y_i + v_00 * (1-d_i) * (1-y_i)
            # custom function
            if config_data.chosen_dataset == config_data.german:
                u_DM *= decision_subject['credit_amount']
            expected_utility_DM += u_DM
            counter_DM += 1

            if J(decision_subject):
                # calculate the decision subject utility
                u_DS = w_11 * d_i * y_i + w_10 * d_i * \
                    (1-y_i) + w_01 * (1-d_i) * y_i + w_00 * (1-d_i) * (1-y_i)
                expected_utility_DS += u_DS
                counter_DS += 1

    if (counter_DM != 0):
        expected_utility_DM /= counter_DM
    if (counter_DS != 0):
        expected_utility_DS /= counter_DS

    return expected_utility_DM, expected_utility_DS, counter_DM


def evaluate_model(all_data):
    U_DM_A0 = {}  # decision maker utility group 0
    U_DM_A1 = {}  # decision maker utility group 1
    U_DS_A0 = {}  # decision subject utility group 0
    U_DS_A1 = {}  # decision subject utility group 1

    if decision_rules == 'linear-lower':
        threshold_function = get_thresholds_linear
    elif decision_rules == 'linear-upper-and-lower':
        threshold_function = get_upper_and_lower_bound_thresholds
    elif decision_rules == 'quantile-based-lower':
        threshold_function = get_thresholds_quantile_based
    elif decision_rules == 'quantile-based-upper-and-lower':
        threshold_function = get_upper_and_lower_bound_thresholds_quantile_based

    thresholds = threshold_function(num_thresholds, all_data["p"])

    # calculate DM- and DS-utility for group 0
    for threshold_0 in thresholds:
        U_DM_r_A0, U_DS_r_A0, n_A0 = calculate_utilities(all_data, 0, threshold_0)
        U_DS_A0[threshold_0] = U_DS_r_A0
        U_DM_A0[threshold_0] = U_DM_r_A0

    # calculate DM- and DS-utility for group 1
    for threshold_1 in thresholds:
        U_DM_r_A1, U_DS_r_A1, n_A1 = calculate_utilities(all_data, 1, threshold_1)
        U_DS_A1[threshold_1] = U_DS_r_A1
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
        # make sure that higher fairness scores are better
        max_FS = max(FS)
        FS = [max_FS - f for f in FS]
    return U_DM_all_thresholds, U_DS_A0_all_thresholds, U_DS_A1_all_thresholds, FS


def is_pareto_efficient(points, return_mask=True):
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
    while next_point_index < len(points):
        nondominated_point_mask = np.any(points > points[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        # Remove dominated points
        is_efficient = is_efficient[nondominated_point_mask]
        points = points[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1
    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype=bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient
