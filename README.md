# A Justice-Based Framework for the Analysis of Algorithmic Fairness-Utility Trade-Offs

This repository is the official implementation of the paper "A Justice-Based Framework for the Analysis of Algorithmic Fairness-Utility Trade-Offs" by Corinna Hertweck,\* Joachim Baumann,\* Michele Loi and Christoph Heitz (\*equal contribution).
The paper describes an approach for balancing the utility of the decision maker and the fairness towards the decision subjects for a prediction-based decision-making system. It also includes concepts presented in the paper "Distributive Justice as the Foundational Premise of Fair ML: Unification, Extension, and Interpretation of Group Fairness Metrics" by Joachim Baumann,\* Corinna Hertweck,\* Michele Loi and Christoph Heitz (\*equal contribution), which proposes a general framework for analyzing the fairness of decision systems based on theories of distributive justice and which unifies and extends existing definitions of group fairness criteria.

## Requirements

To install requirements, you should have Anaconda installed. Once installed, run:

```setup
conda env create -f environment.yml
conda activate utility-based-fairness
```

## Data

The datasets can be found in the folder `/data` and are taken from [Friedler et al. (2019)](https://github.com/algofairness/fairness-comparison).

## Create a different fairness criterion

The Pareto plot shown in ``Plots.ipynb`` shows how well a specific fairness criterion is fulfilled. This fairness criterion can be edited by making changes to the ``config_approach.py``. The dataset on which the fairness is measured can be edited in ``config_data.ipynb``. After making such changes, rerun the notebook ``Plots.ipynb``.

## Plots

To plot the figures shown in the paper ``Plots.ipynb``.
