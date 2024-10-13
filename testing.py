import random_walk
import configparser
import numpy as np
import random
import pytest
from hypothesis import strategies as st
from hypothesis import given, settings

config = configparser.ConfigParser()
config.read('configuration_test.txt')

# Extract values from the configuration
N_config = int(config['settings']['N'])
M_config = int(config['settings']['M'])
n_max_config = int(config['settings']['n_max'])
time_steps_config = int(config['settings']['time_steps'])
collection_time_config = int(config['settings']['collection_time'])

@given(N=st.integers(min_value=0, max_value=N_config), 
       M=st.integers(min_value=0, max_value=n_max_config), 
       n_max=st.integers(min_value=1, max_value=n_max_config))
@settings(max_examples=50)
def test_initialize_network(N, M, n_max):
    """
    Test the `initialize_network` function.

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles in each node at the start.
        n_max (int): Maximum allowed particles per node.

    Tests:
        The function raises a `ValueError` when `N < 1` or `M < 1`.
        The function raises a `ValueError` when `M > n_max`.
        The network has the correct number of nodes.
        Each node is initialized with the correct number of particles.
    """
    if N < 1 or M < 1:
        # If N or M are smaller than one, a ValueError should be raised
        with pytest.raises(ValueError):
            random_walk.initialize_network(N, M, n_max)
    elif M > n_max:
        # If M is greater than n_max, a ValueError should be raised
        with pytest.raises(ValueError):
            random_walk.initialize_network(N, M, n_max)
    else:
        network = random_walk.initialize_network(N, M, n_max)
        # Test the network has the correct number of nodes
        assert len(network) == N
        # Test each node has M particles at the moment of initialization
        assert all(state == M for state in network)


def test_get_neighbor_index():
    """
    Test the `get_neighbor_index` function with explicit direction values (0 for left, 1 for right).
    Given the current node and the direction of movement.
    Used before the movement is performed.
    
    Tests:
        The function correctly calculates the neighboring node's index for any node for both directions
    """
    for N in range(1, N_config):
        for current_node in range(0, N):
            # Test for direction = 1 (moving to the right)
            direction = 1
            neighbor_index = random_walk.get_neighbor_index(current_node, N, direction)
            expected_neighbor = (current_node + 1) % N
            # Test neighbor index is within bounds
            assert 0 <= neighbor_index < N  
            # Test correct neighbor is returned
            assert neighbor_index == expected_neighbor  
            # Test for direction = 0 (moving to the left)
            direction = 0
            neighbor_index = random_walk.get_neighbor_index(current_node, N, direction)
            expected_neighbor = (current_node - 1) % N
            # Test neighbor index is within bounds
            assert 0 <= neighbor_index < N  
            # Test correct neighbor is returned
            assert neighbor_index == expected_neighbor  


@given(N=st.integers(min_value=1, max_value=N_config),  
       M=st.integers(min_value=1, max_value=M_config),
       n_max=st.integers(min_value=M_config, max_value=n_max_config))
@settings(max_examples=5, deadline=None)
def test_move_particle(N, M, n_max):
    """
    Test the `move_particle` function.

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles per node at the start.
        n_max (int): Maximum number of particles a node can hold.

    Tests:
        The number of particles is conserved before and after the exchange.
        The state of each node is never negative.
        The state of each node surpasses n_max by at most one.
        At most one particle moves for each exchange.
    """
    # Initialize network with N nodes, M particles
    network_before = random_walk.initialize_network(N, M, n_max)
    for current_node in range(N):
        for direction in [0, 1]: 
            # Determine the neighbor node based on the current direction
            neighbor = random_walk.get_neighbor_index(current_node, N, direction)
            # Move a particle from current_node to its neighbor
            updated_network = random_walk.move_particle(network_before, current_node, neighbor)
            # Test total number of particles is conserved in the exchange
            total_particles_before = sum(network_before)
            total_particles_after = sum(updated_network)
            assert total_particles_before == total_particles_after
            # Test no node has a negative number of particles
            assert all(p >= 0 for p in updated_network)
            # Test the capacity is respected
            assert all(p <= n_max + 1 for p in updated_network)
            for node in range(N):
                # Test at most one particle has moved
                assert np.abs(network_before[node] - updated_network[node]) <= 1


@given(N=st.integers(min_value=1, max_value=N_config),
       M=st.integers(min_value=1, max_value=M_config), 
       n_max=st.integers(min_value=M_config, max_value=n_max_config), 
       time_steps=st.integers(min_value=1, max_value=time_steps_config),
       collection_time=st.integers(min_value=1, max_value=collection_time_config))
@settings(max_examples=5, deadline=None)
def test_synchronous_simulation(N, M, n_max, time_steps, collection_time):
    """
    Test the `synchronous_simulation` function

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles per node at the start.
        n_max (int): Maximum number of particles a node can hold.
        time_steps (int): Number of simulation time steps.

    Tests:
        The function raises a `ValueError` when `collection_time` >= `time_steps`
        The number of particles is conserved throughout the simulation
        The state of each node is never negative
        The state of each node surpasses n_max by at most one
        At most one particle moves for each timestep
        At a time t at most 2t particles have moved
    """
    initial_network = random_walk.initialize_network(N, M, n_max)
    if collection_time >= time_steps:
        with pytest.raises(ValueError):
            random_walk.synchronous_simulation(initial_network, n_max, time_steps, collection_time)
    else:  
        history = random_walk.synchronous_simulation(initial_network, n_max, time_steps, collection_time)
        # Test that the total number of particles is conserved
        total_particles_initial = sum(initial_network)
        total_particles_final = sum(history[-1])
        assert total_particles_initial == total_particles_final
        # Test that the particles per node are within valid bounds 
        for state in history:
            # Ensure no node exceeds the maximum allowed particles
            assert all(p <= n_max + 1 for p in state)
            # Ensure no node has negative particles
            assert all(p >= 0 for p in state)
        for time in range(2, len(history)):
            prev_state = history[time - 1]
            current_state = history[time]
            for node in range(N):
                # Test at most one particle has moved in successive timesteps
                assert np.abs(current_state[node] - prev_state[node]) <= 2 
                # Test at most one particle per timestep has moved since the beginning
                assert np.abs(current_state[node] - history[1][node]) <= 2 * time
             
               
@given(N=st.integers(min_value=1, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config),
    n_max=st.integers(min_value=M_config, max_value=n_max_config),
    time_steps=st.integers(min_value=1, max_value=time_steps_config),
    collection_time=st.integers(min_value=1, max_value=collection_time_config))
@settings(max_examples=5, deadline = None)
def test_one_step_process(N, M, n_max, time_steps, collection_time):
    """
    Test the `one_step_process` function

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles per node at the start.
        n_max (int): Maximum number of particles a node can hold.
        time_steps (int): Number of simulation time steps.

    Tests:
        The function raises a `ValueError` when `collection_time` >= `time_steps`
        The number of particles is conserved throughout the simulation
        The state of each node is never negative
        The state of each node surpasses n_max by at most one
        At most one particle moves for each timestep
        At time t at most t particles have moved
    """
    initial_network = random_walk.initialize_network(N, M, n_max)
    if collection_time >= time_steps:
        with pytest.raises(ValueError):
            random_walk.synchronous_simulation(initial_network, n_max, time_steps, collection_time)
    else:  
        initial_network = random_walk.initialize_network(N, M, n_max)
        history = random_walk.one_step_process(initial_network, n_max, time_steps, collection_time)
        # Test that the total number of particles is conserved
        total_particles_initial = sum(initial_network)
        total_particles_final = sum(history[-1])
        assert total_particles_initial == total_particles_final
        for state in history:
            # Test the capacity is respected
            assert all(p <= n_max for p in state)
            # Test no node has a negative number of particles
            assert all(p >= 0 for p in state)
        for time in range(2, len(history)):
            prev_state = history[time - 1]
            current_state = history[time]
            for node in range(N):
                # Test at most one particle has moved in successive timesteps
                assert np.abs(current_state[node] - prev_state[node]) <= 1
                # Test at most one particle per timestep has moved since the beginning
                assert np.abs(current_state[node] - history[1][node]) <= time
