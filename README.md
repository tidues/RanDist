# Distance between Random Events

This package is for symbolically and numerically calculating the arbitrary order moments, pdf, cdf and their conditional counterparts of the distance between two random events in a given graph. The position of an event in a network is encoded in a tuple `(e, p)`, where `e={u,v}` (assume `u < v`) is the edge where the event happens and `p` is the relative location of the event on that edge, that is the length of the segment from `u` (the vertex with small index) to the location of the event divided by the length of the edge `e`. Since both events are random, we use `(X, P)` and `(Y, Q)` to denote both events respectively.


## Installation

Use pip to install the randist package.
```
pip install randist
```

## Inputs
1. A data file whose rows are edges of the network with extra properties. There are five columns,
   * `i`: first vertex of the edge
   * `j`: second vertex of the edge
   * `l`: length of the current edge
   * `x`: the probability of event 1 happens on the current edge
   * `y`: the probability of event 2 happens on the current edge

2. The joint distribution of the relative locations of two events, ![alt text](https://latex.codecogs.com/gif.latex?\Phi_\scriptscriptstyle{P,Q}(p,q)). This should be provided as a `Phi` object,
```
from sympy.abc import p, q  # import symbols
import randist as rt        # import our randist package

phi_pq = 1  # the uniform distribution
phi_pq = 36 * p * (1 - p) * q * (1 - q)  # both are beta functions with parameters alpha = beta = 2

phi = rt.Phi('betapq', phi_pq=phi_pq)  # create a Phi object with a name

```
In current implementation, the random variables `X` and `Y` are assumed to be independent, but the formulas we developed in our paper do not have this restriction. Also, currently, we assume the joint pdf ![alt text](https://latex.codecogs.com/gif.latex?\Phi_\scriptscriptstyle{P,Q}(p,q)) are same for all pair of edges `(e, f)`, but the formulas in our paper do not have this restriction. We may relax both restrictions in the future version.

Also notice the input joint distribution `phi_pq` does not have to be correct outside of the domain `[0, 1]^2` the unit square in the `pq`-plane (all values should be zero outside this domain). Our package will verify whether the input expression integral to `1` in its domain, but will not verify the non-negative requirement.

## Outputs
Several statistics about the random distance `D` between two events:
1. moments of arbitrary order 
2. cdf (point evaluation, or plotting against the distance `x`) 
3. pdf (point evaluation, or plotting against the distance `x`) 
4. conditional moments of arbitrary order  (point evaluation, or plotting against the relative location `p` given `X=e`) 
5. conditional cdf  (point evaluation or plotting against `x` given `(X, P) = (e, p)` ) 
6. conditional pdf  (point evaluation or plotting against `x` given `(X, P) = (e, p)` )

All these statistics can be computed either symbolically or numerically. We will explain their differences later.

## Main Interfaces
User can achieve most tasks with two interfaces, `Formulas` and `data_collector`. The former gives the freedom of calculating statistics individually, where the latter can collect data in batch.

### Interface 1: `Formulas` Object

#### Example
An example of using formulas objects to compute statistics:
```
from sympy.abc import p, q  # import symbols
import randist as rt        # import our package

gname = 'g0'  # data file name in the folder ./data
phi_pq = 36 * p * (1-p) * q * (1 - q)
phi = rt.Phi('betapq', phi_pq=phi_pq)  # create a joint pdf with a name

fls = rt.Formulas(gname, phi)                 # create a formulas object

moment = fls.get_formula(rt.Stats.MOMENT)     # get a moment formula object
cdf = fls.get_formula(rt.Stats.CDF)           # get a cdf formula object
pdf = fls.get_formula(rt.Stats.PDF)           # get a cdf formula object
cmoment = fls.get_formula(rt.Stats.MOMENT)    # get a moment formula object
ccdf = fls.get_formula(rt.Stats.CCDF)         # get a cdf formula object
cpdf = fls.get_formula(rt.Stats.CPDF)         # get a cdf formula object

moment.eval(3)                        # computing the 3rd order moment
moment.eval(2) - moment.eval(1) ** 2  # compute the variance
cdf.eval(9.5)                         # evaluate the cdf at the point x = 9.5
cdf.plot(show=True)                   # save the plot in the ./results folder and show it
pdf.eval(8.1)                         # evaluate the pdf at the point x = 9.5
pdf.plot()                            # save the plot in the ./results folder without showing
cmoment.eval(1, ('1', '2'), 0.5)      # the conditional expectation given (e, p) = (('1', '2'), 0.5)
cmoment.plot(2, ('1', '2'))           # plot the conditional 2nd moment against the value of p
ccdf.eval(('2', '3'), 0.1, 3.5)       # evaluate the conditional cdf at x = 3.5 given (e, p) = (('2', '3'), 0.1)
ccdf.plot(('2', '3'), 0.1)            # plot the conditional cdf given (e, p) = (('2', '3'), 0.1)
cpdf.eval(('2', '3'), 0.1, 3.5)       # same but with conditional pdf
cpdf.plot(('2', '3'), 0.1)            # same but with conditional pdf
```

#### The `Formulas` Class
The `Formulas` class has the following parameters,
```
Formulas(gname, phi, fpath='./data/', rational=False, d_jit=False, memorize=True)
```
each parameter is explained below:
* gname:    data file name without the extension `.dat`
* phi:      a Phi object for input joint distribution
* fpath:    the folder where you put the input data file
* rational: if `True`, all value are computed in the rational form (slow)
* d_jit: compute the shortest path length between pair of vertices in a `Just In Time` fashion. Set this to `True` if the input graph is very large and only conditional statistics are needed.
* memorize: use memorization to speedup the computation. Set this to `False` only if the input graph is too large so that the memories in the computer are not enough.

#### The `get_formula` Function
```
get_formula(stats, symbolic=None)
```
each parameter is explained below:
1. stats: specify which type of formulas you want, all types are in the enum type Stats.
2. symbolic: calculate values numerically or symbolically. The default value `None` means auto, so moments and conditional moments will be calculated numerically, and all the rest are calculated symbolically.

#### Comparison between Numeric and Symbolic Formulas
1. Symbolic formula object is slow in generating the formula, but fast in evaluating values once the formula has been generated.
2. Symbolic formula object has two more methods that numerical formulas do not have, `formula()` which shows the closed-form formula for the corresponding statistics, and `save_formula()` that saves the generated formula into file, so that users can load it by the function `load_formulas` in the future without generating the formulas from scratch again.
3. Symbolic formula is faster in plotting.
4. One drawback is that the speed of symbolic formulas are getting much more slower when the size of the graph increase.
5. Numeric formulas are fast in evaluating a single value. And it performs much faster than symbolic formulas in both plotting and evaluation when graph is large.

Basically, if the network is large, always use numeric formulas. Otherwise, please use the default setting, especially if you want to reuse the formulas in the future.

### Interface 2: `data_collector` Function
Basically, the function `data_collector` is a wrapper of the `Formulas` class. We will demonstrate the usage with an example.

#### Example

```
from sympy.abc import p, q  # import symbols
import randist as rt        # import our randist package

gname = 'g0'                # input graph name
phi = rt.Phi('uniform', 1)  # creating a input joint distribution

ks = [1, 2, 3]              # list of orders for moments
loc1 = (('1', '2'), 0.2)
loc2 = (('1', '3'), 0.5)
loc3 = (('3', '4'), 0)
locs = [loc1, loc2, loc3]   # list of locations

mmtp = {'collect': True, 'symbolic': None, 'valst': ks}          # params for moment
cdfp = {'collect': True, 'symbolic': None}                       # params for cdf

pdfp = {'collect': True, 'symbolic': None}                       # params for pdf
cmmtp ={'collect': True, 'symbolic': None, 'valst': (ks, locs)}  # params for conditional moment
ccdfp = {'collect': True, 'symbolic': None, 'valst': locs}       # params for conditional cdf
cpdfp = {'collect': True, 'symbolic': False, 'valst': locs}      # params for conditional pdf

d_jit = False     # whether compute pairwise shortest distance in a Just In Time fashion
memorize = True   # whether use memorization to speedup the computation

# collect all specified data and save them in the folder ./results
rt.data_collector(gname, phi, mmtp, cdfp, pdfp, cmmtp, ccdfp, cpdfp, d_jit=d_jit, memorize=memorize)   
```

## Future Plan
1. Remove the current restrictions mentioned before about `X` and `Y`, and ![alt text](https://latex.codecogs.com/gif.latex?\Phi_\scriptscriptstyle{P,Q}(p,q)).
2. Interactive user interface.
