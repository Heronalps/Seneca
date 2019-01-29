import re
from contextlib import redirect_stdout

def parse(file_path, output_path):
    scores = []
    count = 0
    with open(file_path, 'w') as result:
        with redirect_stdout(result):
            with open(output_path, 'a') as f:
                line = f.readline()
                print (line)
                while line:
                    count = count + 1
                    print ("count : {0}".format(count))
                    match = re.search("Accuracy Score: (0\.\d*)", line)
                    if match:
                        score = float(match.group(1))
                        print ("score : {0}".format(score))
                        scores.append(score)
                    line = f.readline()
        print ("The max accuracy score : {0}".format(max(scores)))

if __name__ == "__main__":
    parse("./XGBoost/xgb_output_cp.txt", "./xgboost.txt")