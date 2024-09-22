import random_walk
import configparser
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

@given(N=st.integers(min_value=2, max_value=N_config), 
       M=st.integers(min_value=1, max_value=M_config))
@settings(max_examples=5)
def test_initialize_network(N, M):
    network = random_walk.initialize_network(N, M)
    
    # Check that the network has the correct number of nodes
    assert len(network) == N, f"Expected {N} nodes, but got {len(network)}."
    
    # Check that each node has M particles
    assert all(particles == M for particles in network), f"Expected each node to have {M} particles."

