import matplotlib.pyplot as plt
import json

def plot_curve(x_series, y_series, num):
    x_point = []
    y_point = []
    path = str("./sampling{0}.data".format(num))
    
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            hash = json.loads(line)
            x_point.append(hash[x_series])
            y_point.append(1 / hash[y_series])
            line = f.readline()
    # print(x_point)
    # print(y_point)

    fig, ax = plt.subplots()
    # plt.ylim(0, 140)    
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel(x_series)
    plt.ylabel(y_series)
    plt.title("{0} VS {1}".format(x_series, "computing power"), fontsize=10)
    plt.plot(x_point, y_point, 'b-')
    

if __name__ == '__main__':
    plot_curve('memory_size', 'billed_duration', 4)