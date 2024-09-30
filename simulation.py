import random_walk
import configparser
import numpy as np
import sys
import random
from sys import argv

# Load configuration
config = configparser.ConfigParser()
config.read(sys.argv[1])

# Read parameters from the configuration file
N = config.getint('settings', 'N')
M = config.getint('settings', 'M')
n_max = config.getint('settings', 'n_max')
time_steps = config.getint('settings', 'time_steps')
dynamics_type = config.get('settings', 'dynamics_type')  
seed_value = config.get('settings', 'seed_value')  

random.seed(seed_value)

# Get paths from the configuration file
simulation_data_path = config.get('paths', 'simulation_data')

# Initialize the network
network = random_walk.initialize_network(N, M, n_max)

# Run the simulation based on the dynamics type
if dynamics_type == 'synchronous':
    particle_counts = random_walk.synchronous_simulation(network, n_max, time_steps)
elif dynamics_type == 'one_step':
    particle_counts = random_walk.one_step_process(network, n_max, time_steps)
else:
    raise ValueError("Invalid dynamics type specified in configuration file.")

# Save results for plotting
with open(simulation_data_path, 'wb') as f:
    np.save(f, particle_counts)
