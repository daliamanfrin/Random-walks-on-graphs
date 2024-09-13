import configparser
from randomwalk import initialize_network, synchronous_simulation, one_step_process, random_direction
import numpy as np

# Load configuration
config = configparser.ConfigParser()
config.read('C:/Users/Dalia/Desktop/project/configuration.txt')

# Read parameters from the configuration file
num_nodes = config.getint('Simulation', 'num_nodes')
initial_particles = config.getint('Simulation', 'initial_particles')
n_max = config.getint('Simulation', 'n_max')
num_time_steps = config.getint('Simulation', 'num_time_steps')
n_movers = config.getint('Simulation', 'n_movers')
dynamics_type = config.get('Simulation', 'dynamics_type')  # 'synchronous' or 'one_step'

# Initialize the network
network = initialize_network(num_nodes, initial_particles)

# Run the simulation for valid dynamics type
if dynamics_type == 'synchronous':
    particle_counts = synchronous_simulation(network, num_nodes, n_movers, n_max, num_time_steps, random_direction)
elif dynamics_type == 'one_step':
    particle_counts = one_step_process(network, num_nodes, n_movers, n_max, num_time_steps, random_direction)
else:
    raise ValueError("Invalid dynamics type specified in configuration file.")

# Save results for plotting
with open('C:/Users/Dalia/Desktop/project/particle_counts.npy', 'wb') as f:
    np.save(f, particle_counts)
