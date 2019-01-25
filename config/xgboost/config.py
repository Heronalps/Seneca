# Hyperparameters
class Hyperparameter:
    MAX_DEPTH = [1, 2]
    LEARNING_RATE = [0.01, 0.02]
    N_ESTIMATORS = [2, 3]
    BOOSTER = ['gbtree', 'gblinear', 'dart']
    N_JOBS = [2]
    GAMMA = [0.1]
    MIN_CHILD_WEIGHT = [2]
    MAX_DELTA_STEP = [5]
    SUBSAMPLE = [0.1]
    COLSAMPLE_BYTREE = [0.2]
    COLSAMPLE_BYLEVEL = [0.2]
    REG_ALPHA = [0.2]
    REG_LAMBDA = [0.1]
    SCALE_POS_WEIGHT = [0.3]
    BASE_SCORE = [10]
    RANDOM_STATE = [123]

class Config:
    # The Dataset filename 
    DATASET = 'data_2017.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'XGBoost_worker'