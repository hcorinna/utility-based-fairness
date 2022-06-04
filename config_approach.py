# Utility of the decision maker (as v_dy, for decisions d and individuals of type y)
v_11 = 0.1
v_10 = -1
v_01 = 0
v_00 = 0

# Utility of the decision subjects (as w_dy, for decisions d and individuals of type y)
w_11 = 10
w_10 = 5
w_01 = -1
w_00 = 0

# Relevant positions

## Claims differentiator
### Define a lambda function that takes in the data of a decision subject and outputs whether the individual is in J
### Returns true or false
J = lambda decision_subject: decision_subject['Y'] == 1

## Sources of inequality
### The name of the (binary) sensitive variable A
A = 'sex'

# Relation to inequality
### Options are: 'egalitarianism', 'maximin', 'prioritarianism', 'sufficientarianism'
EGALITARIANISM = 'egalitarianism'
MAXIMIN = 'maximin'
PRIORITARIANISM = 'prioritarianism'
SUFFICIENTARIANISM = 'sufficientarianism'
pattern = MAXIMIN

## Weight for worst-off group in prioritarianism (is not used if a pattern other than prioritarianism is chosen)
k = 2

## Minimum level of utility for sufficientarianism (is not used if a pattern other than sufficientarianism is chosen)
s = 0.5

# Number of thresholds tested for each group
num_thresholds = 101