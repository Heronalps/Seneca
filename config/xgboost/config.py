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
    # COLSAMPLE_BYTREE = [1]
    # COLSAMPLE_BYLEVEL = [1]
    # REG_ALPHA = [0]
    # REG_LAMBDA = [1]
    # MIN_CHILD_WEIGHT = [1]
    # MAX_DELTA_STEP = [0]
    # SCALE_POS_WEIGHT = [1]
    # BASE_SCORE = [0.5]
    # RANDOM_STATE = [123]
    
    MAX_DEPTH = [3, 4]
    LEARNING_RATE = [0.1, 0.01]
    N_ESTIMATORS = [100, 400]
    # reg:linear, reg:logistic, binary:logistic, binary:logitraw, 
    # count:poisson, multi:softmax, multi:softprob, rank:pairwise
    OBJECTIVE= ['reg:linear', 'rank:pairwise'] 
    BOOSTER = ['gbtree', 'gblinear', 'dart']
    N_JOBS = [1]
    GAMMA = [0]
    MIN_CHILD_WEIGHT = [0.1, 1]
    MAX_DELTA_STEP = [0, 5]
    SCALE_POS_WEIGHT = [1, 2]
    # COLSAMPLE_BYTREE = [0.2, 0.5]
    # COLSAMPLE_BYLEVEL = [0.2, 0.5]
    # REG_ALPHA = [0.1, 0.9]
    # REG_LAMBDA = [0.1, 0.9]
    BASE_SCORE = [0.5, 10]
    RANDOM_STATE = [123]

class Config:
    # The Dataset filename 
    DATASET = 'df_2017_downsampled.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'XGBoost_worker'

    # Test size
    TEST_SIZE = 0.2
