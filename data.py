import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def get_train_test_data(dataset_info):
    X, y = get_X_y(dataset_info)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    scale_data(X_train, X_test, dataset_info['numerical_attributes'])
    return X_train, X_test, y_train, y_test

def get_X_y(dataset_info):
    filename, target = dataset_info['filename'], dataset_info['Y']
    df = pd.read_csv('data/' + filename)
    y = df[target]
    y = y.replace(to_replace=2, value=0, inplace=False)
    X = df.drop([target], axis=1)
    return X, y

def scale_data(X_train, X_test, numerical):
    scaler = StandardScaler()
    
    scaler.fit(X_train[numerical])
    
    X_train[numerical] = scaler.transform(X_train[numerical])
    X_test[numerical] = scaler.transform(X_test[numerical])