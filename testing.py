import random_walk
import configparser
import numpy as np
import hypothesis
from hypothesis import strategies as st
from hypothesis import assume
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
    time_steps=st.integers(min_value=1000, max_value=time_steps_config),
    direction=st.integers(min_value=0, max_value=1) )
@settings(max_examples=5, deadline=None)
def test_synchronous_simulation(N, M, n_max, time_steps, direction):
    initial_network = random_walk.initialize_network(N, M, n_max) 
    def fixed_direction():
        return direction  # Always return the fixed direction (0 or 1) 
    history = random_walk.synchronous_simulation(initial_network, n_max, time_steps, fixed_direction)
    #Test the total number of particles is conserved
    total_particles_initial = sum(initial_network)
    total_particles_final = sum(history[-1])
    assert total_particles_initial == total_particles_final
    for state in history:
        # For synchronous process, the maximum number of particles can be exceeded by 1
        assert all(p <= n_max + 1 for p in state)
        #Test that the number of particles in a node is never negative
        assert all(p >= 0 for p in state)
    for time in range(1, len(history)):
        prev_state = history[time - 1]
        current_state = history[time]
        for node in range(N):
            neighbor = random_walk.get_neighbor_index(node, N, direction)
            if prev_state[node] > 0 and prev_state[neighbor] < n_max:
                # Test at most a particle has moved
                assert np.abs(current_state[node] - prev_state[node]) <= 2
                assert np.abs(current_state[neighbor] - prev_state[neighbor]) <= 2 


@given(N=st.integers(min_value=1, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config),
    n_max=st.integers(min_value=M_config, max_value=n_max_config),
    time_steps=st.integers(min_value=1, max_value=time_steps_config),
    direction=st.integers(min_value=0, max_value=1))
@settings(max_examples=5, deadline = None)
def test_one_step_process(N, M, n_max, time_steps, direction):
    initial_network = random_walk.initialize_network(N, M, n_max)
    # Define a fixed direction function based on the input direction
    def fixed_direction():
        return direction  # Always return the fixed direction (0 or 1)
    # Get the history of particle movements
    history = random_walk.one_step_process(initial_network, n_max, time_steps, fixed_direction)
    # Test the total number of particles is conserved
    total_particles_initial = sum(initial_network)
    total_particles_final = sum(history[-1])
    assert total_particles_initial == total_particles_final
    for state in history:
        # For one step process, the maximum number of particles should never be exceeded
        assert all(p <= n_max for p in state)
        # The number of particles in any node should never be negative
        assert all(p >= 0 for p in state)
    for time in range(1, len(history)):
        prev_state = history[time - 1]
        current_state = history[time]
        for node in range(N):
            neighbor = random_walk.get_neighbor_index(node, N, direction)
            if prev_state[node] > 0 and prev_state[neighbor] < n_max:
                # Test at most a particle has moved
                assert np.abs(current_state[node] - prev_state[node]) <= 1
                assert np.abs(current_state[neighbor] - prev_state[neighbor]) <= 1 
 
@given(
    N=st.integers(min_value=2, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config),
    n_max=st.integers(min_value=M_config, max_value=n_max_config),
    current_node=st.integers(min_value=1, max_value=N_config),
    direction=st.integers(min_value=0, max_value=1)
)
@settings(max_examples=5, deadline=None)
def test_move_particle(N, M, n_max, current_node, direction):
    current_node = current_node % N
    network_before = random_walk.initialize_network(N, M, n_max)
    neighbor = random_walk.get_neighbor_index(current_node, N, direction)
    # Only move particles if the current node has particles and the neighbor has space
    assume(network_before[current_node] > 0)
    assume(network_before[neighbor] < n_max)
    updated_network = random_walk.move_particle(network_before, current_node, neighbor)
    # Test total number of particles is conserved in the movement
    total_particles_before = sum(network_before)
    total_particles_after = sum(updated_network)
    assert total_particles_before == total_particles_after
    # Ensure no node has a negative number of particles
    assert all(p >= 0 for p in updated_network)
