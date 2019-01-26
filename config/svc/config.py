# Hyperparameters
class Hyperparameter:
    C = [1.0]
    KERNEL = [] # linear, poly, rbf, sigmoid, precomputed

class Config:
    # The Dataset filename 
    DATASET = 'df_2017_reduced.csv'

    # Lambda Function Name
    LAMBDA_NAME = 'svc_worker'