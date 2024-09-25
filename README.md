# Random walks on graphs
The aim of this work is to explore the behavior of movement of particles in a simple network. The network is 2-regular graph, linear disposition of nodes with periodic boundary conditions, a structure equivalent to a ring. The particles perform a random walk across nodes: through the edges part of the population can travel among the linked nodes.<br/> 
In this network, the random walk behavior represents an equal probability for a particle to move either to its left or right neighboring node. 
This random walk can be simulated in two different types of dynamics: one-step or synchronous. In the one-step approximation, the evolution is the one-step master equation: <br /> 

<p align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial\rho}{\partial&space;t}(\vec{n},t)=\sum_{i,j}[E^-_{i}E^&plus;_{j}\pi_{ij}(n_{j})-\pi_{ji}(n_{i})]\rho(\vec{n},t)" title="\frac{\partial\rho}{\partial t}(\vec{n},t)=\sum_{i,j}[E^-_{i}E^+_{j}\pi_{ij}(n_{j})-\pi_{ji}(n_{i})]\rho(\vec{n},t)" />
</p>

and the information is instaneously updated after a single node performs movement.
The synchronous dynamics is less explored and it is not trivial to write a ME. In this setting, the network state is updated only after all the nodes have performed their movement. 
To model congestion effects, transport and storage capacity are to be constrained meaning that only a finite number of particles can be sent from
one node to another connected node at a time, and that up to a finite number of particle
can stack on the same node at the same time (capacity constraint).
When the number of moving particles per node is small with respect to the number of particles initially posed on each node, the stationary distributions depends solely on the relation between the initial number of particles and the maximal occupancy. Three distinct distributions are identified based on different initial occupancies: occupancy close to $0$, close to the capacity, and half the capacity. 
For the one-step process, it can be shown that the three solutions can be derived from the maximum entropy principle.


The code initializes the network with given parameters and performs a random walk based on the type of chosen dynamics. For each timestep, it cycles through the nodes. For each node, the moving particles randomly choose a neighbor and jump to it if its occupancy is less than the maximal one. If the chosen number of moving particles are available, they all move, else only the ones available move. Depending on the dynamics, after every movement or after every node has performed a movement, the network is updated and the state (occupancy) for each node are counted. What we get is a histogram that represent the most likely states through the simulation.
## Structure
- The file [random_walk](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/random_walk.py) contains the definition of all the functions, from the initialization of the network to the definition of the random walk. Functions include the generation of a random direction, the choice of the neighbor based on that direction, and the definition of a function for performing the jumps for a single node (`move_particles`). Finally the two functions for the types of dynamics, which both use `move_particles`.

- The [testing](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/testing.py) file tests the functions in the previous file, using hypotesis, to ensure correct behavior. Can be run with pytest.

- The [configuration](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/configuration.txt) file contains the definitions of the parameters used in the simulation: number of nodes (`N`) and initial number of particle per node (`M`) define the network. Then simulation parameters, the number of particles allowed to move for each node (`n_movers`), number of timesteps (`num_time_steps`), maximal occupancy (`n_max`). The type of dynamics is to be chosen between `one_step` and `synchronous`. Lastly the paths can be set up to save results data and plots. 

- The file [simulation](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/simulation.py) contains the main part of the code. The ConfigParser library is used in order to import the configuration file from command line, and passing its parameters to the program. For every iteration or timestep, random walk is performed for the occupants of the nodes, based on the chosen type of dynamic. The state of each node (the number of particles it contains) is computed and saved. Then, the distribution of the states is obtained. 

- The file [plots](https://github.com/daliamanfrin/Random-walks-on-graphs/blob/main/plot.py) contains the function that plots the counts of the states of nodes through the iterations. It uses the data generated during the simulation and saved. The paths to save the plot can be decided in configuration.txt. 


## Usage
To use the program:
1. Choose desired configuration in the configuration file. Edit the existent one or create a new one following the same template, choosing parameters values, dynamics type and paths for saving intermediate results and plots.
2. Run the simulation file with first argument the configuration file, for example: 
```
python simulation.py configuration.txt
```
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This produces and saves a file (default is **particle_counts.npy**) with stored particle counts.
 
3. To visualize the distributions plot, run the plotting file using the produced data. Syntax is, like before 
```
python plot.py configuration.txt
```
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp; Here data is loaded from path provided in the configuration file through local paths and then are saved in the images folder.

### Example
Examples of results valid if the case `n_movers`$\ll$`M` where the dynamics depends solely on the relation between `M` and `n_max`.
Images show distributions for one-step process (top) and synchronous dynamics (bottom) for a half-filled, almost empty and almost congested networks.
Note that in the synchronous dynamics, as expected, the theoretical maximal occupancy can be surpassed
![config](./images/resulting_occupancy.png)
