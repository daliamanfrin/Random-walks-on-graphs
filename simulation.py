import random_walk
import configparser
import numpy as np
import sys
from sys import argv

# Load configuration
config = configparser.ConfigParser()
config.read(sys.argv[1])

# Read parameters from the configuration file
N = config.getint('settings', 'N')
M = config.getint('settings', 'M')
n_max = config.getint('settings', 'n_max')
num_time_steps = config.getint('settings', 'num_time_steps')
n_movers = config.getint('settings', 'n_movers')
dynamics_type = config.get('settings', 'dynamics_type')  # 'synchronous' or 'one_step'

# Get paths from the configuration file
simulation_data_path = config.get('paths', 'simulation_data')

# Initialize the network
network = random_walk.initialize_network(N, M)

# Run the simulation based on the dynamics type
if dynamics_type == 'synchronous':
    particle_counts = random_walk.synchronous_simulation(network, N, n_movers, n_max, num_time_steps, random_walk.random_direction)
elif dynamics_type == 'one_step':
    particle_counts = random_walk.one_step_process(network, N, n_movers, n_max, num_time_steps, random_walk.random_direction)
else:
    raise ValueError("Invalid dynamics type specified in configuration file.")

# Save results for plotting
with open(simulation_data_path, 'wb') as f:
    np.save(f, particle_counts)
