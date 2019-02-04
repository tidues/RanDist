# Distance between Random Events

This package is for symbolically and numerically calculating the arbitrary order moments, pdf, cdf and their conditional counterparts of the distance between two random events in a given graph. The position of an event in a network is encoded in a tuple `(e, p)`, where `e={u,v}` (assume `u < v`) is the edge where the event happens and `p` is the relative location of the event on that edge, that is the length of the segment from `u` (the vertex with small index) to the location of the event divided by the length of the edge `e`. Since both events are random, we use `(X, P)` and `(Y, Q)` to denote both events respectively.


## Installation

Use pip to install the randist package
'''
pip install randist
'''

## Inputs
1. A data file whose rows are edges of the network with extra properties. There are five columns,
   * `i`: first vertex of the edge
   * `j`: second vertex of the edge
   * `l`: length of the current edge
   * `x`: the probability of event 1 happens on the current edge
   * `y`: the probability of event 2 happens on the current edge

2. The joint distribution of the relative locations of two events, ![alt text](https://latex.codecogs.com/gif.latex?\Phi_\scriptscriptstyle{P,Q}(p,q)). This should be provided as a sympy expression,
```
from sympy.abc import p, q  # import symbols

phi_pq = 1  # uniform distribution
phi_pq = 36 * p * (1 - p) * q * (1 - q)  # both are beta function with parameters alpha = beta = 2

```

