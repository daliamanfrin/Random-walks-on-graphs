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
    Invalid case: The function raises a `ValueError` when `M > n_max`.
    Valid case: The network has the correct number of nodes (N).
                Each node is initialized with the correct number of particles (M).

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
    # Test both directions 
    for seed_value in [0, 1]: 
        random.seed(seed_value)
        # Generate a random direction (0 or 1) based on the seed
        direction = random.randint(0, 1)
        # Get the neighbor index from the function
        neighbor_index = random_walk.get_neighbor_index(current_node, N, direction)
        # Test that the neighbor index is valid (within bounds of the network)
        assert 0 <= neighbor_index < N
        # Calculate the expected neighbor index based on direction
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
    time_steps=st.integers(min_value=1000, max_value=time_steps_config),
    direction=st.integers(min_value=0, max_value=1))
@settings(max_examples=5, deadline=None)
def test_synchronous_simulation(N, M, n_max, time_steps, direction):
    random.seed(1)
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
       time_steps=st.integers(min_value=1000, max_value=time_steps_config))
@settings(max_examples=5, deadline=None)
def test_synchronous_simulation_with_random_directions(N, M, n_max, time_steps):
    """
    Test the `synchronous_simulation` function

    Args:
    N (int): Number of nodes in the network.
    M (int): Number of particles per node at the start.
    n_max (int): Maximum number of particles a node can hold.
    time_steps (int): Number of simulation time steps.

    Tests
    
    Raises:
    AssertionError: If any condition related to particle conservation, particle movement, 
                    or state limits is violated during the simulation.
    """
    # Initialize the network
    initial_network = random_walk.initialize_network(N, M, n_max)

    # Loop through different seeds to alternate directions (0 = left, 1 = right)
    for seed_value in [42, 43]:
        random.seed(seed_value)
        direction = random.randint(0,1)
        # Run the synchronous simulation
        history = random_walk.synchronous_simulation(initial_network, n_max, time_steps, direction)

        # Test that the total number of particles is conserved throughout the simulation
        total_particles_initial = sum(initial_network)
        total_particles_final = sum(history[-1])
        assert total_particles_initial == total_particles_final, (
            f"Total particles mismatch: {total_particles_initial} != {total_particles_final}"
        )

        # Check that the particles per node are within valid bounds throughout the simulation
        for state in history:
            # Ensure no node exceeds the maximum allowed particles
            assert all(p <= n_max + 1 for p in state), "Node exceeded max particles"
            # Ensure no node has negative particles
            assert all(p >= 0 for p in state), "Negative particles in node"

        # Check particle movement constraints between consecutive time steps
        for time in range(1, len(history)):
            prev_state = history[time - 1]
            current_state = history[time]

            for node in range(N):
                neighbor = random_walk.get_neighbor_index(node, N, random.randint(0,1))

                if prev_state[node] > 0 and prev_state[neighbor] < n_max:
                    # Ensure at most 1 particle has moved between nodes
                    assert np.abs(current_state[node] - prev_state[node]) <= 2, (
                        f"Too many particles moved from node {node} at time {time}"
                    )
                    assert np.abs(current_state[neighbor] - prev_state[neighbor]) <= 2, (
                        f"Too many particles moved to neighbor {neighbor} at time {time}"
                    )


@given(N=st.integers(min_value=1, max_value=N_config),
    M=st.integers(min_value=1, max_value=M_config),
    n_max=st.integers(min_value=M_config, max_value=n_max_config),
    time_steps=st.integers(min_value=1, max_value=time_steps_config),
    direction=st.integers(min_value=0, max_value=1))
@settings(max_examples=5, deadline = None)
def test_one_step_process(N, M, n_max, time_steps, direction):
    random.seed(1)
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
