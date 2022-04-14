import data
from sklearn.linear_model import LogisticRegression

def train_lr(dataset_info):
    X_train, X_test, y_train, y_test = data.get_train_test_data(dataset_info)
    clf = LogisticRegression(random_state=0).fit(X_train, y_train)
    print('Score:', clf.score(X_test, y_test))
    return clf

def get_predictions(clf, X, y):
    """
    Makes predictions for X and puts all data in one file, which is then returned.
    Used to get the data that is then used to evaluate the decision maker utility and fairness score.
    """
    scores = clf.predict_proba(X)
    all_data = X
    all_data['Y'] = y
    all_data['p'] = [score[1] for score in scores]
    return all_data