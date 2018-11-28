# This lambda is for testing the allocated memory optimizer
# It essentially dump 3D matrix data to memory, 
# in order to investigate the convexity of Memory-compute charge curve

import random
random.seed()

def lambda_handler(event, context):
    message_map = {}
    total = int(event['number'])
    
    # Create two matrices with random elements, multiply them and save to a dict
    for n in range(1, total):
        matrix_a = [[[0] * n for i in range(n)] for j in range(n)]
        matrix_b = [[[0] * n for i in range(n)] for j in range(n)]
        matrix_result = [[[0] * n for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    matrix_a[i][j][k] = random.randint(0, 255)
                    matrix_b[i][j][k] = random.randint(0, 255)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        matrix_result[i][j][k] += matrix_a[i][j][l] * matrix_b[i][l][k]
        
        message_map[n] = matrix_result
    # print(message_map)
    return {'total': total, 'status': 'Task completed!'}