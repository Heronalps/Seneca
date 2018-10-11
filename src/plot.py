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

    sample_size = str(len(data))
    max_data = str(round(max(data), 3))
    min_data = str(round(min(data), 3))
    mean_data = str(round(mean(data), 3))
    std_data = str(round(std(data), 3))
    
    metrics = "sample size = " + sample_size + \
              ", max = " + max_data + \
              ", min = " + min_data + \
              r'$,  \mu = ' + mean_data + \
              r',\ \sigma = $' + std_data
    # print(metrics)
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, _bins, _patches = plt.hist(x=data, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Host Execution Time (millisec)')
    plt.ylabel('Frequency')
    plt.title('Histogram - Async Celery, Async Lambda, Invocation = 5\n' + metrics, fontsize=10)
    
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

    sns.set_style('darkgrid')
    plt.title("Kernel Distribution Estimate - CA5LA")
    plt.xlabel('Host Execution Time (sec)')
    plt.ylabel('Probability Density')
    sns.distplot(data)
    plt.show() 

def mean(data):
    return float(sum(data) / len(data))

def std(data):
    return stdev(data)

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
    plot_dist("../result/RC_metrics_CA5LA_20181006.data", 'host_execu_time')
