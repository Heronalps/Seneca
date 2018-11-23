import numpy as np
import matplotlib.pyplot as plt
import json, re
from datetime import datetime

# def mean(data):
#     return float(sum(data) / len(data))

# path1 = "./syslog_t2micro2.data"
# # path2 = "./result/metrics_CA6LA_20181023.data"

# data1 = []

# with open(path1, 'r') as f:
# 	line = f.readline()
# 	while line:
# 		total_time = re.search(r'(?<=total\stime\s:\s)(\d\.\d*)', line)
# 		if total_time:
# 			data1.append(float(total_time.group(0)))
# 		line = f.readline()

# print("======Average========")
# # print(mean(data1))

# 1 Test - t3.nano
# 2018-11-02 15:40:54.092788
# 2018-11-02 15:57:22.346447

# 2 Test - t3.nano
# 2018-11-02 17:00:35.814247
# 2018-11-02 17:17:21.500047

# Test - t2.nano
# 2018-11-02 18:19:50.737641
# 2018-11-02 18:36:24.393388

# 1 Test - t2.micro
# 2018-11-02 19:09:40.987295
# 2018-11-02 19:25:34.518139

# 2 Test - t2.micro
# 2018-11-02 19:31:42.085595
# 2018-11-02 19:48:37.016643

# Test 1 - m5
# 2018-11-03 00:08:10.411568
# 2018-11-03 00:08:48.550620

# Test 2 - m5
# 2018-11-03 00:10:33.363975
# 2018-11-03 00:11:08.888945

# Test 3 - m5
# 2018-11-03 00:13:17.034685
# 2018-11-03 00:13:49.249318

# Test 4 - m5
# 2018-11-03 00:14:47.154385
# 2018-11-03 00:15:20.534538

# Test 5 - m5
# 2018-11-03 00:15:51.251050
# 2018-11-03 00:16:22.188727





start = datetime.strptime("2018-11-03 00:15:51.251050", "%Y-%m-%d %H:%M:%S.%f")
end = datetime.strptime("2018-11-03 00:16:22.188727", "%Y-%m-%d %H:%M:%S.%f")
print((end - start).total_seconds() / 600)


