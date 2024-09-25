# Random walks on graphs
The aim of this work is to explore the behavior of movement of particles in a simple network. The particles perform a random walk across nodes. This structure can be used to model real life situations, for example traffic dynamics. Nodes can be used to represent the transport facilities of the network such as roads, highways, airports and so on; and through the edges all or part of the population can travel among the linked nodes.<br/> 
In particular, the network considered in this work is a 2-regular graph: a linear disposition of nodes with periodic boundary conditions, a structure equivalent to a ring. In this case, the random walk behavior represents an equal probability for a particle to move either to its left or right neighboring node. The evolution of a distribution function for some simple cases can be written like the one-step master equation: <br /> 

<p align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial\rho}{\partial&space;t}(\vec{n},t)=\sum_{i,j}[E^-_{i}E^&plus;_{j}\pi_{ij}(n_{j})-\pi_{ji}(n_{i})]\rho(\vec{n},t)" title="\frac{\partial\rho}{\partial t}(\vec{n},t)=\sum_{i,j}[E^-_{i}E^+_{j}\pi_{ij}(n_{j})-\pi_{ji}(n_{i})]\rho(\vec{n},t)" />
</p>

The simplest case for a random walk on a graph is for ISTC (infinite storage and transport capacity) networks, where there is no limitation to the number of particles that nodes can contain and the number of particles that links can transport. 
To model congestion effects, transport and storage capacity are to be constrained. 
This type of networks have both a finite transportation capacity (FTC) and finite
storage capacity (FSC), meaning that only a finite number of particles can be sent from
one node to another connected node at a time, and that up to a finite number of particle
can stack on the same node at the same time.
These boundaries can be modeled using a Heaviside Theta function in the master equation.
In this case the behavior of the system depends on the number of particles initially posed on the network.
If the particles are initially uniformly distributed among nodes, three distinct scenarios are identified based on the initial number of particles on the network: nodes close to an occupancy of $0$, nodes close to the storage capacity limit, and nodes in the middle. 


# Structure
The file [random_walk](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/random_walk.py) contains the definition of all the functions, from the initialization of the network to the definition of the random walk. In particular, it includes different functions for the type of dynamics performed that has to be selected by the user (in configuration.txt) between one_step_process and synchronous_dynamics. 

The [testing](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/testing.py) file tests the functions in the previous file, using hypotesis, to ensure correct behavior. Can be run with pytest.

The [configuration](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/configuration.txt) file contains the definitions of the parameters used in the simulation, such as number of nodes, initial number of particle per node (supposing uniform distibution), the number of particles allowed to move for each node, for each timestep; but also the type of dynamics (one_step/synchronous_dynamics), the paths to save and load results data and plots. 

The file [simulation](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/simulation.py) contains the main part of the code. The ConfigParser library is used in order to import the configuration file from command line, and passing its parameters to the program. For every iteration or time step, random walk is performed for the occupants of the nodes, based on the chosen typ eof dynamic: for each node the state each node is in (the number of particles it contains) is computed and saved. Then, the distribution of the states is obtained. 

The file [plots](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/plot.py) contains the function that plots the counts of the states (from 0 to n_max) a node can be in. It uses the data generated during the simulation and saved. The paths of data and plots are stored in configuration.txt. 


# Usage
To use the program:
1. Choose desired configuration (both parameters and dynamics type) in configuration file. Edit the existent one or create a new one following the same template, choosing parameters values, dynamics type and paths for saving intermediate results and plots.
2. Run the simulation file with first argument the configuration file, for example 
```
python simulation.py configuration.txt
```
 This produces and saves a file (particle_counts.npy) with stored particle counts.
4. To visualize the distribution of abundances plot, run the plotting file using the produced data. Syntax is, like before 
```
python plot.py configuration.txt
```
 Here data is loaded from the configuration file through local paths and then are saved in the images folder.
