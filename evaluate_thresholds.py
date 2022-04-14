from config_approach import *
import config_data
import train
import data
import calculate_utilities
import pattern_functions
import oapackage

def to_threshold(r, number_of_thresholds):
    threshold = (1/(number_of_thresholds-1)) * r
    return round(threshold, 2)

def evaluate_model(all_data):
    U_DM = []
    U_DS_A0 = []
    U_DS_A1 = []
    FS = []
    for i in range(num_thresholds):
        r = to_threshold(i, num_thresholds)
        U_DM_r = calculate_utilities.U_DM(all_data, r)
        U_DM.append(U_DM_r)
        U_DS_r_A0 = calculate_utilities.U_DM(all_data, 0, r)
        U_DS_A0.append(U_DS_r_A0)
        U_DS_r_A1 = calculate_utilities.U_DM(all_data, 1, r)
        U_DS_A1.append(U_DS_r_A1)
        compare_utilities_function = pattern_functions.get_pattern_function()
        FS_r = compare_utilities_function(U_DS_r_A0, U_DS_r_A1)
        FS.append(FS_r)
    return U_DM, U_DS_A0, U_DS_A1, FS

def calculate_pareto_front(FS, U_DM):
    pareto=oapackage.ParetoDoubleLong()

    for i in range(len(FS)):
        w = oapackage.doubleVector((FS[i], U_DM[i]))
        pareto.addvalue(w, i)

    pareto.show(verbose=1)
    
    pareto_list = pareto.allindices()
    return pareto_list

import matplotlib.pyplot as plt
import numpy as np

dataset_info = config_data.chosen_dataset
X_train, X_test, y_train, y_test = data.get_train_test_data(dataset_info)
clf = train.train_lr(dataset_info)
all_data = train.get_predictions(clf, X_train, y_train)

U_DM, U_DS_A0, U_DS_A1, FS = evaluate_model(all_data)
pareto_front_indices = calculate_pareto_front(FS, U_DM)
pareto_list = list(pareto_front_indices)
plt.plot(np.array(FS)[pareto_list].tolist(), np.array(U_DM)[pareto_list].tolist())
# TODO instead of red, iterate over color map and use those colors for bar chart
color_values = ['red' if p in pareto_front_indices else 'black' for p in range(len(FS))]
plt.scatter(FS, U_DM, c=color_values)

# TODO bar charts in different colors for DS utilities of pareto front