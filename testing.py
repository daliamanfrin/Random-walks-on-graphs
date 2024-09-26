import random_walk
import configparser
import numpy as np
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings

# Load the configuration from the txt file
def load_configuration(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

config = load_configuration('configuration.txt')

# Extract values from the configuration
N_config = int(config['settings']['N'])
M_config = int(config['settings']['M'])
n_max_config = int(config['settings']['n_max'])
time_steps_config = int(config['settings']['time_steps'])

@given(N=st.integers(min_value=1, max_value=N_config), 
       M=st.integers(min_value=1, max_value=M_config),
       n_max=st.integers(min_value=M_config, max_value=n_max_config))
@settings(max_examples=5)
def test_initialize_network(N, M, n_max):
    # Initialize the network with N nodes and M particles
    network = random_walk.initialize_network(N, M, n_max)
    # Test that the network has the correct number of nodes
    assert len(network) == N
    # Test that each node has M particles at the momemnt of initialization
    assert all(state == M for state in network)
        
@given(current_node=st.integers(min_value=1, max_value=N_config),
    N=st.integers(min_value=1, max_value=N_config),
    direction=st.integers(min_value=0, max_value=1))
@settings(max_examples=5)
def test_get_neighbor_index(current_node, N, direction):
    current_node = current_node % N
    neighbor_index = random_walk.get_neighbor_index(current_node, N, direction)
    # Test for valid index
    assert 0 <= neighbor_index < N
    if direction == 1:
        # Moving to the right, so the neighbor should be (current_node + 1) % N
        expected_neighbor = (current_node + 1) % N
    else:
        # Moving to the left, so the neighbor should be (current_node - 1) % N
        expected_neighbor = (current_node - 1) % N
    #Test the correct neighbor is returned
    assert neighbor_index == expected_neighbor

@given(N=st.integers(min_value=1, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config), 
    n_max=st.integers(min_value=M_config, max_value=n_max_config), 
    time_steps=st.integers(min_value=1000, max_value=time_steps_config))
@settings(max_examples=5)
def test_synchronous_simulation(N, M, n_max, time_steps):
    initial_network = random_walk.initialize_network(N, M, n_max)  
    history = random_walk.synchronous_simulation(initial_network, n_max, time_steps, random_walk.random_direction)
    #Test the total number of particles is conserved
    total_particles_initial = sum(initial_network)
    total_particles_final = sum(history[-1])
    assert total_particles_initial == total_particles_final
    #Test that the number of particles in a node is never negative
    for state in history:
        assert all(p >= 0 for p in state)

@given(N=st.integers(min_value=1, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config), 
    n_max=st.integers(min_value=M_config, max_value=n_max_config), 
    time_steps=st.integers(min_value=1000, max_value=time_steps_config))
@settings(max_examples=5)
def test_one_step_process(N, M, n_max, time_steps):
    initial_network = random_walk.initialize_network(N, M, n_max)  
    history = random_walk.one_step_process(initial_network, n_max, time_steps, random_walk.random_direction)
    #Test that the total number of particles is conserved
    total_particles_initial = sum(initial_network)
    total_particles_final = sum(history[-1])
    
    assert total_particles_initial == total_particles_final
    for state in history:
        #For one step process the maximum number of particles can never be exceeded
        assert all(p <= n_max for p in state)
        #Test that the number of particles in a node is never negative
        assert all(p >= 0 for p in state)

# # @given(
# #     N=st.integers(min_value=1, max_value=N_config),
# #     n_max=st.integers(min_value=M_config, max_value=n_max_config),
# #     time_steps =st.integers(min_value=250, max_value=time_steps_config)
# # )
# # @settings(max_examples=5)
# # def test_move_particles(N,M, n_movers,n_max, time_steps):
# #     network = random_walk.initialize_network(N, M)
# #     # Copy the initial state for comparison  
# #     initial_state = network.copy()  
# #     # Simulate move_particles function 
# #     for _ in range(time_steps):
# #         for current_node in range(N):
# #             network = random_walk.move_particles(network, current_node, n_movers, n_max, random_direction=lambda: 1, update_network=network.copy())
# #     #Test total number of particles is conserved
# #     assert sum(network) == sum(initial_state) 
