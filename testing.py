import random_walk
import configparser
import numpy as np
import random
import pytest
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
       M=st.integers(min_value=1, max_value=n_max_config), 
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
        The function raises a `ValueError` when `M > n_max`.
        The network has the correct number of nodes.
        Each node is initialized with the correct number of particles.
    """
    if M > n_max:
        # If M is greater than n_max, a ValueError should be raised
        with pytest.raises(ValueError):
            random_walk.initialize_network(N, M, n_max)
    else:
        network = random_walk.initialize_network(N, M, n_max)
        # Test the network has the correct number of nodes
        assert len(network) == N
        # Test each node has M particles at the moment of initialization
        assert all(state == M for state in network)


@given(N=st.integers(min_value=1, max_value=N_config))  
@settings(max_examples=5)
def test_get_neighbor_index(N):
    """
    Test the `get_neighbor_index` function.

    Args:
        N (int): Total number of nodes in the network.

    Tests:
        The function correctly calculates the neighboring node's index for any node for both directions
    """
    current_node = random.randint(0,N)
    for seed_value in [0, 1]: 
        random.seed(seed_value)
        direction = random.randint(0, 1)
        neighbor_index = random_walk.get_neighbor_index(current_node, N, direction)
        # Test that the neighbor index is valid (within bounds of the network)
        assert 0 <= neighbor_index < N
        if direction == 1:
            # Moving to the right: neighbor should be (current_node + 1) % N
            expected_neighbor = (current_node + 1) % N
        else:
            # Moving to the left: neighbor should be (current_node - 1) % N
            expected_neighbor = (current_node - 1) % N 
        # Test that the correct neighbor is returned
        assert neighbor_index == expected_neighbor


@given(N=st.integers(min_value=1, max_value=N_config),
       M=st.integers(min_value=1, max_value=M_config), 
       n_max=st.integers(min_value=M_config, max_value=n_max_config), 
       time_steps=st.integers(min_value=1000, max_value=time_steps_config))
@settings(max_examples=5, deadline=None)
def test_synchronous_simulation(N, M, n_max, time_steps):
    """
    Test the `synchronous_simulation` function

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles per node at the start.
        n_max (int): Maximum number of particles a node can hold.
        time_steps (int): Number of simulation time steps.

    Tests:
        The number of particles is conserved throughout the simulation
        The state of each node is never negative
        The state of each node surpasses n_max by at most one
        At most one particle moves for each timestep
        At a time t at most 2t particles have moved
    """
    initial_network = random_walk.initialize_network(N, M, n_max)
    for seed_value in [0, 1]:
        random.seed(seed_value)
        direction = random.randint(0, 1)
        history = random_walk.synchronous_simulation(initial_network, n_max, time_steps)
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
    time_steps=st.integers(min_value=1000, max_value=time_steps_config))
@settings(max_examples=5, deadline = None)
def test_one_step_process(N, M, n_max, time_steps):
    """
    Test the `one_step_process` function

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles per node at the start.
        n_max (int): Maximum number of particles a node can hold.
        time_steps (int): Number of simulation time steps.

    Tests:
        The number of particles is conserved throughout the simulation
        The state of each node is never negative
        The state of each node surpasses n_max by at most one
        At most one particle moves for each timestep
        At time t at most t particles have moved
    """
    initial_network = random_walk.initialize_network(N, M, n_max)
    for seed_value in [0, 1]:
        random.seed(seed_value)
        direction = random.randint(0, 1)
        history = random_walk.one_step_process(initial_network, n_max, time_steps)
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
 
@given(
    N=st.integers(min_value=1, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config),
    n_max=st.integers(min_value=M_config, max_value=n_max_config))
@settings(max_examples=5, deadline=None)
def test_move_particle(N, M, n_max):
    """
    Test the `move_particle` function

    Args:
        N (int): Number of nodes in the network.
        M (int): Number of particles per node at the start.
        n_max (int): Maximum number of particles a node can hold.

    Tests:
        The number of particles is conserved before and after the exchange
        The state of each node is never negative
        The state of each node surpasses n_max by at most one
        At most one particle moves for each exchange
    """
    current_node = random.randint(0, N-1)
    for seed_value in [0, 1]:
        random.seed(seed_value)
        direction = random.randint(0, 1)
        network_before = random_walk.initialize_network(N, M, n_max)
        neighbor = random_walk.get_neighbor_index(current_node, N, direction)  
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
