# Hyperparameters
class Hyperparameter:
    HIDDEN_LAYER_SIZES = [[100,2]]
    ACTIVATION = ['relu'] # identity, logistic, tanh, relu
    SOLVER = ['adam'] # lbfgs, sgd, adam
    ALPHA = [0.0001]
    BATCH_SIZE = [200]
    LEARNING_RATE = ['constant'] # constant, invscaling, adaptive
    LEARNING_RATE_INIT = [0.001]
    POWER_T = [0.5]
    MAX_ITER = [200]
    SHUFFLE = [True]
    RANDOM_STATE = [123]
    TOL = [1e-4]
    MOMENTUM = [0.9]
    EARLY_STOPPING = [False]
    VALIDATION_FRACTION = [0.1]
    BETA_1 = [0.9]
    BETA_2 = [0.999]
    EPSILON = [1e-8]
    N_ITER_NO_CHANGE = [10]
    VERBOSE = [True]



class Config:
    # The Dataset filename 
    DATASET = 'df_2017_reduced.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'neural_network_worker'