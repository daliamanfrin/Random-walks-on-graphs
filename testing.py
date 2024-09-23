import random_walk
import configparser
import numpy as np
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings
from unittest.mock import patch


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
num_time_steps_config = int(config['settings']['num_time_steps'])
n_movers_config = int(config['settings']['n_movers'])


@given(N=st.integers(min_value=2, max_value=N_config), 
       M=st.integers(min_value=1, max_value=M_config))
@settings(max_examples=5)
def test_initialize_network(N, M):
    try:
        # Normal case: Valid values for N and M
        network = random_walk.initialize_network(N, M)

        # Check that the network has the correct number of nodes
        if len(network) != N:
            raise ValueError(f"Expected {N} nodes, but got {len(network)}.")

        # Check that each node has M particles
        if not all(particles == M for particles in network):
            raise ValueError(f"Expected each node to have {M} particles.")
        
    except ValueError as e:
        # Edge case handling: Check invalid N or M
        if N <= 1:
            assert str(e) == f"N must be > 1. Received: {N}"
        elif M < 1:
            assert str(e) == f"M must be >= 1. Received: {M}"
        else:
            raise  RuntimeError("Unexpected error occurred.")

@given(
    current_node=st.integers(min_value=1, max_value=N_config),
    N=st.integers(min_value=2, max_value=N_config),
    direction=st.integers(min_value=0, max_value=1)
)
@settings(max_examples=5)
def test_get_neighbor_index(current_node, N, direction):
    # Ensure current_node is within bounds of the network
    current_node = current_node % N
    
    # Call the function being tested
    neighbor_index = random_walk.get_neighbor_index(current_node, N, direction)
    
    # Check for valid return values
    assert 0 <= neighbor_index < N, f"Neighbor index {neighbor_index} is out of bounds for network size {N}."
    
    if direction == 1:
        # Moving to the right, so the neighbor should be (current_node + 1) % N
        expected_neighbor = (current_node + 1) % N
    else:
        # Moving to the left, so the neighbor should be (current_node - 1) % N
        expected_neighbor = (current_node - 1) % N

    assert neighbor_index == expected_neighbor, (
        f"Expected neighbor index {expected_neighbor}, but got {neighbor_index} "
        f"for current_node {current_node}, N {N}, direction {direction}."
    )

def test_random_direction():
    """
    Test that random_direction function works correctly when mocked.
    """
    with patch('random_walk.random_direction') as mock_random:
        # Mock to always return 0 (direction: left)
        mock_random.return_value = 0
        result = random_walk.random_direction()
        assert result == 0, f"Expected 0, but got {result}"

        # Mock to always return 1 (direction: right)
        mock_random.return_value = 1
        result = random_walk.random_direction()
        assert result == 1, f"Expected 1, but got {result}"

@given(
    N=st.integers(min_value=2, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config), 
    n_movers=st.integers(min_value=1, max_value=n_movers_config),  
    n_max=st.integers(min_value=1, max_value=n_max_config), 
    num_time_steps=st.integers(min_value=1, max_value=num_time_steps_config) 
)
@settings(max_examples=5)
def test_synchronous_simulation(N, M, n_movers, n_max, num_time_steps):
    # Create initial network with random particle counts
    initial_network = random_walk.initialize_network(N, M)  
    
    history = random_walk.synchronous_simulation(initial_network, N, n_movers, n_max, num_time_steps, random_walk.random_direction)
    
    # Check that the history length matches the number of time steps
    assert len(history) == num_time_steps, "History length does not match the number of time steps."
    
    # Check that the total number of particles is conserved
    total_particles_initial = sum(initial_network)
    total_particles_final = sum(history[-1])
    assert total_particles_initial == total_particles_final, "Total number of particles should be conserved."
    
    # Check that no node exceeds the maximum number of particles allowed and the number of particles is never negative
    for state in history:
        assert all(p >= 0 for p in state), f"Particle count is negative in state {state}."

@given(
    N=st.integers(min_value=2, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config), 
    n_movers=st.integers(min_value=1, max_value=n_movers_config),  
    n_max=st.integers(min_value=M_config, max_value=n_max_config), 
    num_time_steps=st.integers(min_value=1, max_value=num_time_steps_config) 
)
@settings(max_examples=5)
def test_one_step_process(N, M, n_movers, n_max, num_time_steps):
    # Create initial network with random particle counts
    initial_network = random_walk.initialize_network(N, M)  
    
    history = random_walk.one_step_process(initial_network, N, n_movers, n_max, num_time_steps, random_walk.random_direction)
    
    # Check that the history length matches the number of time steps
    assert len(history) == num_time_steps * N, "History length does not match the expected number of time steps."
    
    # Check that the total number of particles is conserved
    total_particles_initial = sum(initial_network)
    total_particles_final = sum(history[-1])
    assert total_particles_initial == total_particles_final, "Total number of particles should be conserved."
    
    # Check that no node exceeds the maximum number of particles allowed and the number of particles is never negative
    for state in history:
        assert all(p <= n_max for p in state), f"Particle count exceeds n_max in state {state}." # For one step process n max can never be exceeded
        assert all(p >= 0 for p in state), f"Particle count is negative in state {state}."

@given(
    N=st.integers(min_value=2, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config),
    n_movers=st.integers(min_value=1, max_value=n_movers_config),
    n_max=st.integers(min_value=1, max_value=n_max_config),
    num_time_steps =st.integers(min_value=1, max_value=num_time_steps_config)
)
@settings(max_examples=5)
def test_move_particles(N,M, n_movers,n_max, num_time_steps):
    # Set up the network with initial values from the configuration
    network = random_walk.initialize_network(N, M)  # You may define this
    initial_state = network.copy()  # Copy the initial state for comparison

    # Run the `move_particles` function multiple times
    for _ in range(num_time_steps):
        for current_node in range(N):
            network = random_walk.move_particles(network, N,M, n_movers,n_max, num_time_steps,
                                                 random_direction=lambda: 1,  # Example direction mock
                                                )  

    assert sum(network) == sum(initial_state) #Total number of particles should remain constant
