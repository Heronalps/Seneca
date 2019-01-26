# Hyperparameters
class Hyperparameter:
    C = [1.0]
    KERNEL = ['poly'] # linear, poly, rbf, sigmoid, precomputed
    DEGREE = [3]
    GAMMA = ['scale'] # auto, scale
    COEF0 = [0.1]
    SHRINKING = [True]
    PROBABILITY = [False]
    TOL = [1e-3]
    CACHE_SIZE = [5.0]
    VERBOSE = [False]
    MAX_ITER = [20]
    DECISION_FUNCTION_SHAPE = ['ovr'] # one-over-one(ovo), one-over-rest(ovr)
    RANDOM_STATE = [123]

class Config:
    # The Dataset filename 
    DATASET = 'df_2017_reduced.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'svc_worker'