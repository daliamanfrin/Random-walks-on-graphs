import random

def initialize_network(N, M, n_max):
    """
    Initialize the network with a given number of nodes, each having a specified initial particle count.
    
    Args:
    N (int): Number of nodes in the network.
    M (int): Number of particles in each node at the start.
    n_max (int): Maximum allowed particles per node.

    
    Returns:
    list: Initial configuration of the network.
    
    Raises:
    ValueError: If N or M is less than 1, or if M exceeds the maximum allowed value of n_max.

    """
    if N < 1 or M < 1:
        raise ValueError(f"Number of nodes and particles per node should be at least 1, got N = {N} and M = {M}")
    if M > n_max:
        raise ValueError(f"Initial particles per node should be smaller than the maximum capacity, got M = {M} and n_max = {n_max}")

    # Initialize the network with parameters from configuration   
    return [M] * N


def get_neighbor_index(current_node, N, direction):
    """
    Get the index of the neighbor node in a circular network based on the direction of movement.
    
    Args:
    current_node (int): Index of the current node.
    N (int): Number of nodes in the network.
    direction (int): Direction of movement, 0 for left, 1 for right.
    
    Returns:
    int: Index of the neighboring node.
    """
    # Get the neighbor based on the direction of the random walk step
    return (current_node + 1) % N if direction == 1 else (current_node - 1) % N

def move_particle(network, current_node, neighbor):
    """
    Move a particle from the current node to its neighbor and return the updated network.
    
    Args:
    network (list): The current state of the network with particle counts.
    current_node (int): The node from which the particle is moved.
    neighbor (int): The neighboring node to which the particle is moved.
    
    Returns:
    list: The updated network after the particle move.
    """
    # Create a copy of the network (to avoid modifying the original directly)
    updated_network = network.copy()

    # Move a particle from current_node to the neighbor
    updated_network[current_node] -= 1
    updated_network[neighbor] += 1

    return updated_network


def synchronous_simulation(network, n_max, time_steps, random_direction):
    """
    Simulate the particle movement using a synchronous process, where all nodes are updated simultaneously at each time step.

    Args:
    network (list): The initial state of the network with particle counts.
    n_max (int): Maximum allowed particles per node.
    time_steps (int): Number of time steps to simulate.
    random_direction (callable): A function that returns 0 or 1 to determine the direction of particle movement.

    Returns:
    list: History of particle counts for each node at each time step.
    """
    N = len(network)
    particle_counts = []
    particle_counts.append(network.copy())
    for time in range(time_steps):
        update_network = network.copy()  # Copy network for synchronous updates
        for current_node in range(N):
            direction = random_direction()  # Get random direction
            neighbor = get_neighbor_index(current_node, N, direction)  # Get neighbor index

            # Only move if neighbor has capacity
            if network[neighbor] < n_max and network[current_node] > 0:
                update_network = move_particle(update_network, current_node, neighbor)  # Move the particle

        network = update_network  # Update the network with the new state
        if time > 1000:
            particle_counts.append(network.copy())  # Record the network state after 200 time steps

    return particle_counts


def one_step_process(network, n_max, time_steps, random_direction):
    """
    Simulate the particle movement using a one-step process, where the network is updated after each node completes its move.

    Args:
    network (list): The initial state of the network with particle counts.
    n_max (int): Maximum allowed particles per node.
    time_steps (int): Number of time steps to simulate.
    random_direction (callable): A function that returns 0 or 1 to determine the direction of particle movement.

    Returns:
    list: History of particle counts for each node at each time step.
    """
    N = len(network)
    particle_counts = []
    particle_counts.append(network.copy())
    for time in range(time_steps):
        for current_node in range(N):
            if network[current_node] >= 0:
                direction = random_direction()  # Get random direction
                neighbor = get_neighbor_index(current_node, N, direction)  # Get neighbor index

                if network[neighbor] < n_max and network[current_node] > 0:
                    network = move_particle(network, current_node, neighbor)  # Move the particle
                if time > 1000:
                    particle_counts.append(network.copy())  # Record the network state after each move

    return particle_counts  


def random_direction():
    """
    Generate a random direction for particle movement (0 for left, 1 for right).
    
    Returns:
    int: 0 or 1 to determine the direction of particle movement.
    """
    return random.randint(0, 1)
