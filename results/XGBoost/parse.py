import re
from contextlib import redirect_stdout

scores = []
count = 0
with open("./output.txt", 'w') as result:
    with redirect_stdout(result):
        with open("./xgb_output_cp.txt", 'r') as f:
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