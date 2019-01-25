import os, boto3
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import mean_absolute_error

local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('csv'))
client = boto3.client('s3')
s3 = boto3.resource('s3')

def read_csv_s3(file_name):
    if not os.path.exists(local_repo):
        os.makedirs(local_repo)
    path = local_repo + '/' + file_name
    bucket = 'seneca-racelab'
    client.download_file(bucket, file_name, path)
    df = pd.read_csv(path)
    return df

directory_2017 = {
    "Pro_41" : "41N",
    "Pro_43" : "92E",
    "Pro_98_80" : "80",
    "Pro_98_81W" : "81W",
    "Pro_112_Clem_12-11-17" : "64E",
    "Pro_112_Daisy_1-4-18" : "64E",
    "Pro_112_Daisy_12-13-17" : "64E"
}

def lambda_handler(event, context={}):
    # Load parameters
    parameter_list = event['parameters']
    parameters = {}
    for key in parameter_list:
        parameters[key] = event['data'][key]
    
    # df = read_csv_s3(parameters['dataset'])
    df = pd.read_csv("./datasets/neural_network/df_2017_reduced.csv")
    # Scamble and subset data frame into train + validation(80%) and test(10%)
    df = df.sample(frac=1).reset_index(drop=True)
    split_ratio = 0.8
    print('Train and Test Split Ratio : ', split_ratio)
    df_train = df[ : int(len(df) * split_ratio)]
    df_test = df[int(len(df) * split_ratio) : ]

    kf = KFold(n_splits=10)
    solver = MLPClassifier(**parameters)

    # convert dataframe to ndarray, since kf.split returns nparray as index
    feature_train = df_train.iloc[:, 0: -1].values
    target_train = df_train.iloc[:, -1].values
    feature_test = df_test.iloc[:, 0: -1].values
    target_test = df_test.iloc[:, -1].values

    # Train NN with train dataset
    # The classification is random and could be skewed, because the training set is sampled.
    # Generally, it is down to 0.996 accuracy and ~1.0 f1-score for 5 fields.
    
    for train_indices, test_indices in kf.split(feature_train, target_train):
        solver.fit(feature_train[train_indices], target_train[train_indices])
        print(solver.score(feature_train[test_indices], target_train[test_indices]))

    y_pred = solver.predict(feature_test)
    accu_score = accuracy_score(y_pred, target_test)
    print("Accuracy Score : " + str(accu_score))
    print(classification_report(target_test, y_pred))

    
    unique, count = np.unique(target_test, return_counts=True)
    print("Test dataset Distribution")
    print(np.asarray((unique, count)).T)

    unique, count = np.unique(y_pred, return_counts=True)
    print("Prediction dataset Distribution")
    print(np.asarray((unique, count)).T)

    return {'metric': accu_score, 'event': event}