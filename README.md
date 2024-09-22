# Random walks on graphs
The aim of this work is to explore the behavior of movement of particles in a simple network. The particles perform a random walk across nodes. This structure can be used to model real life situations, for example traffic dynamics. Nodes can be used to represent the transport facilities of the network such as roads, highways, airports and so on; and through the edges all or part of the population can travel among the linked nodes.<br/> 
In particular, the network considered in this work is a 2-regular graph: a linear disposition of nodes with periodic boundary conditions, a structure equivalent to a ring. In this case, the random walk behavior represents an equal probability for a particle to move either to its left or right neighboring node. The evolution of a distribution function for some simple cases can be written like the master equation: <br /> 

<p align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial\rho}{\partial&space;t}(\vec{n},t)=\sum_{i,j}[E^-_{i}E^&plus;_{j}\pi_{ij}(n_{j})-\pi_{ji}(n_{i})]\rho(\vec{n},t)" title="\frac{\partial\rho}{\partial t}(\vec{n},t)=\sum_{i,j}[E^-_{i}E^+_{j}\pi_{ij}(n_{j})-\pi_{ji}(n_{i})]\rho(\vec{n},t)" />
</p>

From the ME one gets the stationary state, a solution for which the system maintains a constant probability flux.
The simplest case for a random walk on a graph is for ISTC (infinite storage and transport capacity) networks, where there is no limitation to the number of particles that nodes can contain and the number of particles that links can transport. In this case transition probabilities are independent from the state of the network. This is the case of $n$ non-interacting particles, and we can simulate the solution of the master equation for the average dynamics.
To model congestion effects, we need to move to the case where transport and storage capacity are constrained. In this case the transition rates, and consequently the flow, depend on the state of the graph. In a transport network, this could mean that a street can only allow a certain number of vehicles, an airport a certain number of airplanes and so on. 
This type of networks have both a finite transportation capacity (FTC) and finite
storage capacity (FSC), meaning that only a finite number of particles can be sent from
one node to another connected node at a time, and that up to a finite number of particle
can stack on the same node at the same time.
These boundaries can be modeled using the Heaviside Theta function in the master equation.
After the imposing of constraints, the probability to obtain an empty or a full node are not negligible. In this case the behavior of the system depends on the number of particles initially posed on the network.
If the particles are initially uniformly distributed among nodes, three distinct scenarios are identified based on the initial number of particles on the network: nodes close to an occupancy of $0$, nodes close to the storage capacity limit, and nodes in the middle. Finally, the random walk is simulated to confirm the stationary distribution behavior on the nodes matches the expected theoretical outcomes.


# Structure

The file random_walk contains the definition of all the functions, from the initialization of the network to the simulation of the random walk. For every iteration or time step, random walk is performed, the state each node is in (the number of particles it contains) is computed and saved. Then, the distribution of the states is obtained.

The testing file tests the functions in the previous file, using hypotesis, to ensure correct behavior.

The configuration.txt file contains the definitions of the parameters used in the simulation, such as number of nodes, initial number of particle per node (supposing uniform distibution), the number of particles allowed to move for each node, for each timestep; but also the paths to save and load results data and plots.as number of spins per lattice (N*M), temperature intervals and so on. Furthermore, there are the local paths in order to load the array data and to save them as images and graphs

The file simulation there is the main part of the code, where I have used the functions of ising file in order to calculate the energy and the magnetization of a configuration of spins for a range of temperatures across the critical one Tc, showing a steeply decrease in energy from high temperatures to low ones and a rapidly increase in magnetization, a clear sign of a phase transition. In addition there is the calculation of the different states of the configuration of spins for a given temperatrue, lower than Tc, respect to time, which shows that the system coarsens toward the configuration of all spins aligned; then I saved these states in an array to process them in further data analysis. Here I used the ConfigParser library in order to import the configuration file from command line, and passing its parameters to the program.

The file plots contains the function that plots the counts of the states (from 0 to n_max) a node can be in. It uses the data generated during the simulation and saved. The paths of data and plots are stored in configuration.txt. 

# Usage
To use the program:
1. Choose desired configuration (both parameters and dynamics type) in configuration file. Edit the existent one or create a new one following the same template, choosing parameters values, dynamics type and paths for saving intermediate results and plots.
These are the steps in order to start the program and to plot the results:
2. Run the simulation file with first argument the configuration file, for example "python simulation.py configuration.txt". This produces and saves a file (.npy) with stored particle counts.
4. To visualize the distribution of abundances plot, run the plotting file using the produced data. Syntax is, like before "python plot.py configuration.txt". Here data is loaded from the configuration file through local paths and then are saved in the images folder.
