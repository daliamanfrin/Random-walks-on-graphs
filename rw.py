import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

num_nodes = 20  # M
initial_particles = 2
network = [initial_particles] * num_nodes

N = num_nodes * initial_particles
M = num_nodes

n_max = 20
num_time_steps = 1000

G = nx.cycle_graph(num_nodes)
pos = nx.circular_layout(G)

particle_counts = []

for t in range(num_time_steps):

    new_network = network.copy()

    for i in range(num_nodes):


        if network[i] > 0:

            direction = random.randint(0, 1)  # move left or right (1 right, 0 left)

            if direction == 1:
                neighbor = (i + 1) % num_nodes  
            else:
                neighbor = (i - 1) % num_nodes  

            if network[neighbor] < n_max:
                new_network[i] -= 1
                new_network[neighbor] += 1
            
    network = new_network
    if t % 10 == 0:  # append particle counts every 10 steps
        particle_counts.append(network.copy())
        
flattened_data = [item for sublist in particle_counts for item in sublist]
data = np.array(flattened_data)

d = np.diff(np.unique(data)).min()
left_of_first_bin = data.min() - float(d)/2
right_of_last_bin = data.max() + float(d)/2
plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d, d), edgecolor='black')
plt.show()