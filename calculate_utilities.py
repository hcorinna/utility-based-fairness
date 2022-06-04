import numpy as np
import pandas as pd
from config_approach import *
import config_data

def U_DM(data, A_value, threshold):
    data['D'] = data['p'] >= threshold
    expected_utility = 0
    counter = 0
    for index, decision_subject in data.iterrows():
        if decision_subject[A] == A_value:
            y_i = decision_subject['Y']
            p_i = decision_subject['p']
            d_i = decision_subject['D']
            u_DM = v_11 * d_i * y_i + v_10 * d_i * (1-y_i) + v_01 * (1-d_i) * y_i + v_00 * (1-d_i) * (1-y_i)
            # custom function
            if config_data.chosen_dataset == config_data.german:
                u_DM *= decision_subject['credit_amount']
            expected_utility += u_DM
            counter += 1
    if (counter != 0):
        expected_utility /= counter
    return expected_utility, counter

def U_DS(data, A_value, threshold):
    data['D'] = data['p'] >= threshold
    expected_utility = 0
    counter = 0
    for index, decision_subject in data.iterrows():
        if J(decision_subject) and decision_subject[A] == A_value:
            y_i = decision_subject['Y']
            p_i = decision_subject['p']
            d_i = decision_subject['D']
            u_DS = w_11 * d_i * y_i + w_10 * d_i * (1-y_i) + w_01 * (1-d_i) * y_i + w_00 * (1-d_i) * (1-y_i)
            expected_utility += u_DS
            counter += 1
    if (counter != 0):
        expected_utility /= counter
    return expected_utility