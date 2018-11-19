import json, re

def mean(data):
    return float(sum(data) / len(data))

path1 = "./syslog_m524xlarge5.data"

data1 = []

with open(path1, 'r') as f:
	line = f.readline()
	while line:
		total_time = re.search(r'(?<=total\stime\s:\s)(\d\.\d*)', line)
		if total_time:
			data1.append(float(total_time.group(0)))
		line = f.readline()

print("======Average========")
print(mean(data1))