import random_walk
import configparser
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

@given(N=st.integers(min_value=2, max_value=N_config), 
       M=st.integers(min_value=1, max_value=M_config))
@settings(max_examples=1)
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
            raise  # Unexpected exception


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

