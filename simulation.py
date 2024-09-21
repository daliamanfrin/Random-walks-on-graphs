import random_walk
import configparser
import numpy as np
import sys
from sys import argv


# Load configuration
config = configparser.ConfigParser()
config.read(sys.argv[1])

# Read parameters from the configuration file
num_nodes = config.getint('Simulation', 'num_nodes')
initial_particles = config.getint('Simulation', 'initial_particles')
n_max = config.getint('Simulation', 'n_max')
num_time_steps = config.getint('Simulation', 'num_time_steps')
n_movers = config.getint('Simulation', 'n_movers')
dynamics_type = config.get('Simulation', 'dynamics_type')  # 'synchronous' or 'one_step'

# Initialize the network
network = random_walk.initialize_network(num_nodes, initial_particles)

# Run the simulation for valid dynamics type
if dynamics_type == 'synchronous':
    particle_counts = random_walk.synchronous_simulation(network, num_nodes, n_movers, n_max, num_time_steps, random_walk.random_direction)
elif dynamics_type == 'one_step':
    particle_counts = random_walk.one_step_process(network, num_nodes, n_movers, n_max, num_time_steps, random_walk.random_direction)
else:
    raise ValueError("Invalid dynamics type specified in configuration file.")

# Save results for plotting
with open('C:/Users/Dalia/Desktop/project/particle_counts.npy', 'wb') as f:
    np.save(f, particle_counts)
