import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings
import random_walk 
import configuration  

@given(N=st.integers(1, configuration.max_nodes), M=st.integers(1, configuration.max_particles))
@settings(max_examples=5)
def test_initialize_network(N, M):
    network = random_walk.initialize_network(N, M)
    # Check that the network has the correct number of nodes
    assert len(network) == N
    # Check that each node has M particles
    assert all(particles == M for particles in network)