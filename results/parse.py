import re
from contextlib import redirect_stdout

def parse(file_path, output_path):
    scores = []
    count = 0
    with open(output_path, 'w') as result:
        with redirect_stdout(result):
            with open(file_path, 'r') as f:
                line = f.readline()
                while line:
                    count = count + 1
                    # print ("count : {0}".format(count))
                    match = re.search("Accuracy Score: (0\.\d*)", line)
                    if match:
                        score = float(match.group(1))
                        # print ("score : {0}".format(score))
                        scores.append(score)
                    line = f.readline()
                print (scores)
    print ("The max accuracy score : {0}".format(max(scores)))

if __name__ == "__main__":
    parse("./XGBoost/xgboost_output.txt", "./xgboost.txt")