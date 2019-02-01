# Hyperparameters
class Hyperparameter:
    # Default
    # C = [1.0]
    # KERNEL = ['rbf'] # linear, poly, rbf, sigmoid, precomputed
    # DEGREE = [3]
    # GAMMA = ['auto'] # auto, scale
    # COEF0 = [0.0]
    # SHRINKING = [True]
    # PROBABILITY = [False]
    # TOL = [1e-3]
    # CACHE_SIZE = [5.0]
    # VERBOSE = [False]
    # MAX_ITER = [20]
    # DECISION_FUNCTION_SHAPE = ['ovr'] # one-over-one(ovo), one-over-rest(ovr)
    # RANDOM_STATE = [123]

    C = [0.5, 2.0]
    KERNEL = ['rbf', 'linear', 'poly', 'sigmoid'] # linear, poly, rbf, sigmoid, precomputed
    DEGREE = [2, 4]
    GAMMA = ['auto', 'scale'] # auto, scale
    COEF0 = [-0.5, 0.5]
    SHRINKING = [True]
    PROBABILITY = [False, True]
    TOL = [1e-2, 1e-4]
    CACHE_SIZE = [5.0]
    VERBOSE = [False]
    MAX_ITER = [20]
    DECISION_FUNCTION_SHAPE = ['ovo', 'ovr'] # one-over-one(ovo), one-over-rest(ovr)
    RANDOM_STATE = [123]

class Config:
    # The Dataset filename 
    DATASET = 'df_2017_downsampled.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'svc_worker'

    # Test size
    TEST_SIZE = 0.1
