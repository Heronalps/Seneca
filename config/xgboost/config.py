# Hyperparameters
class Hyperparameter:
    # Default
    # MAX_DEPTH = [3]
    # LEARNING_RATE = [0.1]
    # N_ESTIMATORS = [100]
    # OBJECTIVE= ['reg:linear']
    # BOOSTER = ['gbtree']
    # N_JOBS = [1]
    # GAMMA = [0]
    # MIN_CHILD_WEIGHT = [1]
    # MAX_DELTA_STEP = [0]
    # SUBSAMPLE = [1]
    # COLSAMPLE_BYTREE = [1]
    # COLSAMPLE_BYLEVEL = [1]
    # REG_ALPHA = [0]
    # REG_LAMBDA = [1]
    # SCALE_POS_WEIGHT = [1]
    # BASE_SCORE = [0.5]
    # RANDOM_STATE = [0]
    
    MAX_DEPTH = [2, 4]
    LEARNING_RATE = [0.01, 0.02]
    N_ESTIMATORS = [200, 300]
    # reg:linear, reg:logistic, binary:logistic, binary:logitraw, 
    # count:poisson, multi:softmax, multi:softprob, rank:pairwise
    OBJECTIVE= ['reg:linear', 'rank:pairwise'] 
    BOOSTER = ['gbtree', 'gblinear', 'dart']
    N_JOBS = [4]
    GAMMA = [0.01]
    MIN_CHILD_WEIGHT = [0.1, 2]
    MAX_DELTA_STEP = [2, 5]
    SUBSAMPLE = [0.1, 0.9]
    COLSAMPLE_BYTREE = [0.1, 0.9]
    COLSAMPLE_BYLEVEL = [0.1, 0.9]
    REG_ALPHA = [0.1, 0.9]
    REG_LAMBDA = [0.1, 0.9]
    SCALE_POS_WEIGHT = [0.1, 3]
    BASE_SCORE = [0.1, 10]
    RANDOM_STATE = [123]

class Config:
    # The Dataset filename 
    DATASET = 'data_2017.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'XGBoost_worker'