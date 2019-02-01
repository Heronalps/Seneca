# Hyperparameters
class Hyperparameter:
    # Default
    # HIDDEN_LAYER_SIZES = [(100,)]
    # ACTIVATION = ['relu'] # identity, logistic, tanh, relu
    # SOLVER = ['adam'] # lbfgs, sgd, adam
    # ALPHA = [0.0001]
    # BATCH_SIZE = ['auto']
    # LEARNING_RATE = ['constant'] # constant, invscaling, adaptive
    # LEARNING_RATE_INIT = [0.001]
    # POWER_T = [0.5]
    # MAX_ITER = [20]
    # SHUFFLE = [True]
    # RANDOM_STATE = [123]
    # TOL = [1e-4]
    # MOMENTUM = [0.9]
    # NESTEROVS_MOMENTUM = [True]
    # EARLY_STOPPING = [False]
    # VALIDATION_FRACTION = [0.1]
    # BETA_1 = [0.9]
    # BETA_2 = [0.999]
    # EPSILON = [1e-8]
    # N_ITER_NO_CHANGE = [10]
    # VERBOSE = [False]
    
    HIDDEN_LAYER_SIZES = [(100,)]
    ACTIVATION = ['identity', 'tanh','relu'] # identity, logistic, tanh, relu
    SOLVER = ['lbfgs','sgd','adam'] # lbfgs, sgd, adam
    ALPHA = [0.0001]
    BATCH_SIZE = [200]
    LEARNING_RATE = ['constant', 'invscaling', 'adaptive'] # constant, invscaling, adaptive
    LEARNING_RATE_INIT = [0.001]
    POWER_T = [0.5]
    MAX_ITER = [20]
    SHUFFLE = [True]
    RANDOM_STATE = [123]
    TOL = [1e-3, 1e-5]
    MOMENTUM = [0.9]
    EARLY_STOPPING = [False]
    VALIDATION_FRACTION = [0.1]
    BETA_1 = [0.9]
    BETA_2 = [0.999]
    EPSILON = [1e-8]
    N_ITER_NO_CHANGE = [5, 20]
    VERBOSE = [False]

class Config:
    # The Dataset filename 
    DATASET = 'df_2017_downsampled.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'neural_network_worker'