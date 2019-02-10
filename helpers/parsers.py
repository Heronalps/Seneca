import re, os

def parse_path(current_path, keyword):
    return re.search('.*'+ keyword, current_path).group(0)

def split_path(path):
    # This regex captures filename after the last backslash
    filename = re.search("(?!\/)(?:.(?!\/))*(?=\.\w*$)", path).group(0)
    path_prefix = re.search("(.*\/)(?!.*\/)", path).group(0)
    
    return path_prefix, filename

'''
This function parses string line of REPORT from cloudwatch log and returns dict of 4 metrics
'''

def parse_metrics(message):
    duration = re.search(r'(?<=\tDuration:\s)(.*?)(?=\sms)', message).group(0)
    billed_duration = re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', message).group(0)

    # Megabytes
    memory_size = re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', message).group(0)
    max_memory_used = re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', message).group(0)

    metrics = {
        'Duration': duration,
        'Billed Duration': billed_duration,
        'Memory Size': memory_size,
        'Max Memory Used':max_memory_used
    }
    return metrics


'''
This function parse the cloudwatch log and return a list of specified score
'''

def parse_scores(file_path, pattern="Accuracy Score"):
    scores = []
    count = 0
    with open(file_path, 'r') as f:
        line = f.readline()
        while line:
            count = count + 1
            # print ("count : {0}".format(count))
            match = re.search(pattern + "\s*:* (\d*\.+.*)", line)
            
            if match:
                score = float(match.group(1))
                # print ("score : {0}".format(score))
                scores.append(score)
            line = f.readline()

    return scores

'''
This function parses a single line and returns a dict of pattern and score
'''

def parse_score(line, pattern="Accuracy Score"):
    if line:
        match = re.search(pattern + "\s*:* (\d*\.+.*)", line)  
        if match:
            score = float(match.group(1))
    
    return score
        
    