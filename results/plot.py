import re
from matplotlib import pyplot as plt
from contextlib import redirect_stdout

def parse(file_path):
    scores = []
    count = 0
    print (file_path)
    with open(file_path, 'r') as f:
        line = f.readline()
        while line:
            count = count + 1
            # print ("count : {0}".format(count))
            match = re.search("Accuracy Score\s*: (0\.\d*)", line)
            
            if match:
                score = float(match.group(1))
                # print ("score : {0}".format(score))
                scores.append(score)
            line = f.readline()

    return scores

def plot():
    xgboost_scores = parse("./XGBoost/xgboost_output.txt")
    svc_scores = parse("./svc/svc_output.txt")
    neural_network_scores = parse("./neural_network/neural_network_output.txt")
    
    fig = plt.figure()
    plt.boxplot(xgboost_scores)
    plt.boxplot(svc_scores)
    plt.boxplot(neural_network_scores)
    plt.show()

if __name__ == "__main__":
    plot()