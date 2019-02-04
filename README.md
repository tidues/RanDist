# Distance between Random Events

This package is for symbolically and numerically calculating the arbitrary order moments, pdf, cdf and their conditional counterparts of the distance between two random events in a given graph. The position of an event in a network is encoded in a tuple ![alt text](https://latex.codecogs.com/gif.latex?(e,\&space;p)), where `e={u,v}` (assume `u < v`) is the edge where the event happens and `p` is the relative location of the event on that edge, that is the portion of the length from `u` to the location of the event.


## Installation

Use pip to install the randist package
'''
pip install randist
'''

## Inputs
1. A data file whose rows are edges of the network with extra properties. There are five columns,
   * `i`: start vertex of the edge
   * `j`: end vertex of the edge
   * `l`: length of the current edge
   * `x`: the probability of event 1 happens on the current edge
   * `y`: the probability of event 2 happens on the current edge

2. The joint distribution of the relative locations of two events given both edges where two events happen are fixed, ![alt text](https://latex.codecogs.com/gif.latex?\Phi_{P,Q}(p,q))

