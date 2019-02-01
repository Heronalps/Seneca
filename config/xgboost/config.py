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
    # SCALE_POS_WEIGHT = [1]
    # BASE_SCORE = [0.5]
    # RANDOM_STATE = [123]
    
    MAX_DEPTH = [2, 4]
    LEARNING_RATE = [0.1, 0.01]
    N_ESTIMATORS = [100, 200]
    # reg:linear, reg:logistic, binary:logistic, binary:logitraw, 
    # count:poisson, multi:softmax, multi:softprob, rank:pairwise
    OBJECTIVE= ['reg:linear', 'rank:pairwise'] 
    BOOSTER = ['gbtree', 'gblinear', 'dart']
    N_JOBS = [4]
    GAMMA = [0.01]
    MIN_CHILD_WEIGHT = [0.1, 2]
    MAX_DELTA_STEP = [2, 5]
    SCALE_POS_WEIGHT = [0.1, 2]
    BASE_SCORE = [1, 10]
    RANDOM_STATE = [123]

class Config:
    # The Dataset filename 
    DATASET = 'df_2017_downsampled.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'XGBoost_worker'

    # Test size
    TEST_SIZE = 0.1