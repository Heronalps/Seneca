import random
random.seed()

def lambda_handler(event, context):
    message_map = {}
    total = int(event['number'])
    for n in range(1, total):
        matrix = [[[0] * n for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    matrix[i][j][k] = '{0} {1} {2} {3}...'.format(chr(random.randint(0, 255)),
                                                                  chr(random.randint(0, 255)),
                                                                  chr(random.randint(0, 255)),
                                                                  chr(random.randint(0, 255)))
        message_map[n] = matrix
    print(message_map)
    return {'total': total, 'status': 'Task completed!'}