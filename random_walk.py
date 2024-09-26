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
    ValueError: If N or M are non valid.
    """
    if N < 1 or M < 1:
        raise ValueError(f"Number of nodes and particles per node should be at least 1, got N = {N} and M = {M}")
    # Initialize the network with parameters from configuration   
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
    # Get the neighbor based on the direction of the random walk step
    return (current_node + 1) % N if direction == 1 else (current_node - 1) % N


def move_particles(network, current_node, n_movers, n_max, random_direction, update_network):
    """
    Move a specified number of particles from the current node to its neighboring nodes.
    
    Args:
    network (list): The current state of the network with particle counts.
    current_node (int): Index of the node from which particles are being moved.
    N (int): Total number of nodes in the network.
    n_movers (int): Maximum number of particles that can be moved from the current node.
    n_max (int): Maximum number of particles a neighboring node can hold.
    random_direction (callable): A function that returns 0 or 1 to determine the direction of particle movement.
    update_network (list): The network to update (could be a copy of the original network for synchronous updates).
    
    Returns:
    list: Updated network after attempting to move particles from the current node.
    """
    N = len(network)
    # Determine how many particles move
    movers = min(network[current_node], n_movers)  
    for _ in range(movers):
        # Get the random direction for the walk
        direction = random_direction()  
        # Choose neighbor based the direction
        neighbor = get_neighbor_index(current_node, N, direction)
        # Only move if neighbor has capacity 
        if network[neighbor] < n_max:  
            # Remove a particle from the current node
            update_network[current_node] -= 1 
            # Add a particle to the neighbor
            update_network[neighbor] += 1  
    return update_network


def synchronous_simulation(network, n_movers, n_max, time_steps, random_direction):
    """
    Simulate the particle movement using a synchronous process, where all nodes are updated simultaneously at each time step.
    
    Args:
    network (list): The initial state of the network with particle counts.
    N (int): Total number of nodes in the network.
    n_movers (int): Maximum number of particles that can be moved from each node.
    n_max (int): Maximum number of particles a node can hold.
    time_steps (int): Number of time steps to simulate.
    random_direction (callable): A function that returns 0 or 1 to determine the direction of particle movement.
    
    Returns:
    list: History of particle counts for each node at each time step.
    """
    N = len(network)
    particle_counts = []
    
    for time in range(time_steps):
        new_network = network.copy()  
        for current_node in range(N):
            # Perform movement for a node
            new_network = move_particles(network, current_node, n_movers, n_max, random_direction, new_network)
        # Update the original network after all nodes have moved particles
        network = new_network.copy() 
        # Let the system stabilize 
        if time > 200 : 
            # Save the states after all nodes perform movement
            particle_counts.append(network.copy())  
    
    return particle_counts


def one_step_process(network, n_movers, n_max, time_steps, random_direction):
    """
    Simulate the particle movement using a one-step process, where the network is updated after each node completes its move.
    
    Args:
    network (list): The initial state of the network with particle counts.
    N (int): Total number of nodes in the network.
    n_movers (int): Maximum number of particles that can be moved from each node.
    n_max (int): Maximum number of particles a node can hold.
    time_steps (int): Number of time steps to simulate.
    random_direction (callable): A function that returns 0 or 1 to determine the direction of particle movement.
    
    Returns:
    list: History of particle counts for each node at each time step.
    """
    N = len(network)
    particle_counts = []
    
    for time in range(time_steps):
        for current_node in range(N):
            # Perform movement for a node
            network = move_particles(network, current_node, n_movers, n_max, random_direction, network)
            # Let the system stabilize
            if time > 200 :
                # Update and save the network after each node moves particles
                particle_counts.append(network.copy())  
    
    return particle_counts


def random_direction():
    """
    Generate a random direction for particle movement (0 for left, 1 for right).
    
    Returns:
    int: 0 or 1 to determine the direction of particle movement.
    """
    return random.randint(0, 1)
