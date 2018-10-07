import matplotlib.pyplot as plt
import numpy as np
import json
import seaborn as sns
from statistics import stdev

def plot_hist(path, field):
    data = []
    with open(path, "r") as f:
        line = f.readline()
        while line:
            hash = json.loads(line)
            data.append(hash[field])
            line = f.readline()

    show(data)
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, _bins, _patches = plt.hist(x=data, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.5)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    
    plt.show() 

def plot_dist(path, field):
    data = []
    with open(path, "r") as f:
        line = f.readline()
        while line:
            hash = json.loads(line)
            data.append(hash[field])
            line = f.readline()

    show(data)
    sns.set_style('darkgrid')
    sns.distplot(data)
    plt.show() 

def mean(data):
    return float(sum(data) / len(data))

def std(data):
    return stdev(data)


def show(data):
    print("============Sample Size==================")
    print(len(data))
    print("============Max==========================")
    print(max(data))
    print("============Min==========================")
    print(min(data))
    print("============Mean=========================")
    print(mean(data))
    print("============Standard Deviation===========")
    print(std(data))
    print("=========================================")

# All plotable fields
# "total_duration"
# "total_billed_duration" 
# "max_memory_used" 
# "memory_size" 
# "duration_per_invocation" 
# "compute_charge" 
# "cost" 
# 'host_execu_time'

if __name__ == '__main__':
    plot_dist("./result/metrics_CA100LA_20181007.data", 'host_execu_time')
