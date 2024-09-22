import random_walk 
import configuration
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings

@given(N=st.integers(1, configuration.N), M=st.integers(1, configuration.M))
@settings(max_examples=5)
def test_initialize_network(N, M):
    network = random_walk.initialize_network(N, M)
    
    # Check that the network has the correct number of nodes
    if len(network) != N:
        raise ValueError(f"Expected {N} nodes, but got {len(network)}.")
    
    # Check that each node has M particles
    if not all(particles == M for particles in network):
        raise ValueError(f"Expected each node to have {M} particles.")
