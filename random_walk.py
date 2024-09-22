import random

def initialize_network(N, M):
    """
    Initialize the network with a given number of nodes, each having a specified initial particle count.
    
    Args:
    N (int): Number of nodes in the network.
    M (int): Number of particles in each node at the start.
    
    Returns:
    list: A list representing the initial state of the network.
    
    Raises:
    ValueError: If N or M are degenerate or non valid.
    """
    
    if not isinstance(N, int) or N <= 1:
        raise ValueError(f"N must be > 1. Received: {N}")
    
    if not isinstance(M, int) or M < 1:
        raise ValueError(f"M must be >= 1. Received: {M}")
    
    return [M] * N


def get_neighbor_index(current_node, N, direction):
    """
    Get the index of the neighbor node in a circular network based on the direction of movement.
    
    Args:
    current_node (int): Index of the current node.
    N (int): Total number of nodes in the network.
    direction (int): Direction of movement, 0 for left, 1 for right.
    
    Returns:
    int: Index of the neighboring node.
    """
    return (current_node + 1) % N if direction == 1 else (current_node - 1) % N


def move_particles(network, current_node, N, n_movers, n_max, random_direction_fn):
    """
    Attempt to move a specified number of particles from the current node to its neighboring nodes.
    
    Args:
    network (list): The current state of the network with particle counts.
    current_node (int): Index of the node from which particles are being moved.
    N (int): Total number of nodes in the network.
    n_movers (int): Maximum number of particles that can be moved from the current node.
    n_max (int): Maximum number of particles a neighboring node can hold.
    random_direction_fn (callable): A function that returns 0 or 1 to determine the direction of particle movement.
    
    Returns:
    list: Updated network after attempting to move particles from the current node.
    """
    movers = min(network[current_node], n_movers)
    for _ in range(movers):
        direction = random_direction_fn()  # Use the passed function to get the random direction
        neighbor = get_neighbor_index(current_node, N, direction)
        if network[neighbor] < n_max:
            network[current_node] -= 1
            network[neighbor] += 1
    return network


def synchronous_simulation(network, N, n_movers, n_max, num_time_steps, random_direction_fn):
    """
    Simulate the particle movement using synchronous process, where all nodes are updated simultaneously at each time step.
    
    Args:
    network (list): The initial state of the network with particle counts.
    N (int): Total number of nodes in the network.
    n_movers (int): Maximum number of particles that can be moved from each node.
    n_max (int): Maximum number of particles a node can hold.
    num_time_steps (int): Number of time steps to simulate.
    random_direction_fn (callable): A function that returns 0 or 1 to determine the direction of particle movement.
    
    Returns:
    list: History of particle counts for each node at each time step.
    """
    particle_counts = []
    
    for _ in range(num_time_steps):
        new_network = network.copy()
        for current_node in range(N):
            new_network = move_particles(new_network, current_node, N, n_movers, n_max, random_direction_fn)
        network = new_network
        particle_counts.append(network.copy())
    
    return particle_counts


def one_step_process(network, N, n_movers, n_max, num_time_steps, random_direction_fn):
    """
    Simulate the particle movement using the one-step process, where the network is updated only after all nodes have completed their moves in one time step.
    
    Args:
    network (list): The initial state of the network with particle counts.
    N (int): Total number of nodes in the network.
    n_movers (int): Maximum number of particles that can be moved from each node.
    n_max (int): Maximum number of particles a node can hold.
    num_time_steps (int): Number of time steps to simulate.
    random_direction_fn (callable): A function that returns 0 or 1 to determine the direction of particle movement.
    
    Returns:
    list: History of particle counts for each node at each time step.
    """
    particle_counts = []
    
    for _ in range(num_time_steps):
        for current_node in range(N):
            network = move_particles(network, current_node, N, n_movers, n_max, random_direction_fn)
        particle_counts.append(network.copy())
    
    return particle_counts


# Function to be used during actual simulation, generates a random direction (0 or 1)
def random_direction():
    """
    Generate a random direction for particle movement (0 for left, 1 for right).
    
    Returns:
    int: 0 or 1 to determine the direction of particle movement.
    """
    return random.randint(0, 1)
