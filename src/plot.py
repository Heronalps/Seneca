import matplotlib.pyplot as plt
import numpy as np
import json

def plot(path, field):
        data = []
        with open(path, "r") as f:
            line = f.readline()
            while line:
                hash = json.loads(line)
                data.append(hash[field])
                line = f.readline()
        
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
    plot("./result/metrics_20181006.data", 'total_duration')
