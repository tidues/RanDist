# Distance between Random Events

This package is for symbolically and numerically calculating the arbitrary order moments, pdf, cdf and their conditional counterparts of the distance between two random events in a given graph.

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

2. The joint distribution of the relative locations of two events given both edges where two events happen are fixed, `&Phi_{P,Q}(p,q)`

