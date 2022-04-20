from config_approach import *
import numpy as np


def absolute_difference(utility_A0, utility_A1):
    diff = np.abs(utility_A0 - utility_A1)
    return diff

def min(utility_A0, utility_A1):
    if utility_A0 <= utility_A1:
        return utility_A0
    return utility_A1

def prioritarian_sum(utility_A0, utility_A1):
    if utility_A0 <= utility_A1:
        return utility_A0 * k + utility_A1
    return utility_A0 + utility_A1 * k

def above_threshold(utility_A0, utility_A1):
    groups_above_threshold = 0
    if utility_A0 > s:
        groups_above_threshold += 1
    if utility_A1 > s:
        groups_above_threshold += 1
    return groups_above_threshold

def get_pattern_function():
    compare_utilities_function = None
    if pattern == 'egalitarianism':
        compare_utilities_function = absolute_difference
    if pattern == 'maximin': 
        compare_utilities_function = min
    if pattern == 'prioritarianism':
        compare_utilities_function = prioritarian_sum
    if pattern == 'sufficientarianism':
        compare_utilities_function = above_threshold
    return compare_utilities_function

def get_xlabel():
    label = 'Fairness score:\n'
    if pattern == 'egalitarianism':
        label += 'max difference in expected utility - difference in expected utility'
    if pattern == 'maximin': 
        label += 'Minimum expected utility'
    if pattern == 'prioritarianism':
        label += 'Weighted sum of expected utilities'
    if pattern == 'sufficientarianism':
        label += 'Number of groups with expected utility above threshold'
    return label