import os, boto3
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

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
    
    df = read_csv_s3(event['dataset'])
    # df = pd.read_csv("./datasets/neural_network/df_2017_reduced.csv")
    
    # Scamble and subset data frame into train + validation(80%) and test(10%)
    y = df.block_Num
    X = df.drop(['block_Num'], axis=1).select_dtypes(exclude=['object'])

    feature_train, feature_test, target_train, target_test = train_test_split(X, y, random_state = parameters['random_state'], test_size=event['test_size'])

    # kf = KFold(n_splits=10)
    solver = MLPClassifier(**parameters)

    # Train NN with train dataset
    # The classification is random and could be skewed, because the training set is sampled.
    # Generally, it is down to 0.996 accuracy and ~1.0 f1-score for 5 fields.
    
    solver.fit(feature_train, target_train)
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