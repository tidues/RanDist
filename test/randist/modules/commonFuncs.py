from .pyprelude import FPToolBox as fp
from .pyprelude import TableWriter as tw
from math import factorial
from sympy import *
from sympy.abc import a, b, x
import dill
import networkx as nx
from networkx import is_connected
from scipy.integrate import dblquad

# symbolic gate function
#eta = lambda a, b, x: Piecewise((1, (x >= a) & (x <= b)), (0, True))

class eta(Function):
    nargs = 3

    @classmethod
    def eval(cls, a, b, x):
        if a.is_Number and b.is_Number and x.is_Number:
            zero = numbers.Zero()
            if x >= a and x <= b:
                return 1 + zero
            else:
                return 0 + zero

class etal(Function):
    nargs = 3

    @classmethod
    def eval(cls, a, b, x):
        if a.is_Number and b.is_Number and x.is_Number:
            zero = numbers.Zero()
            if x > a and x <= b:
                return 1 + zero
            else:
                return 0 + zero

class etar(Function):
    nargs = 3

    @classmethod
    def eval(cls, a, b, x):
        if a.is_Number and b.is_Number and x.is_Number:
            zero = numbers.Zero()
            if x >= a and x < b:
                return 1 + zero
            else:
                return 0 + zero
# symbolic theshold function
#theta = lambda a, b, x: Piecewise((a, x < a), (b, x > b), (x, True))

class theta(Function):
    nargs = 3

    @classmethod
    def eval(cls, a, b, x):
        if a.is_Number and b.is_Number and x.is_Number:
            if x < a:
                return a
            elif x >b:
                return b
            else:
                return x

class mmin(Function):
    nargs = 2

    @classmethod
    def eval(cls, a, b):
        if a.is_Number and b.is_Number:
            if a <= b:
                return a
            else:
                return b

class mmax(Function):
    nargs = 2

    @classmethod
    def eval(cls, a, b):
        if a.is_Number and b.is_Number:
            if a >= b:
                return a
            else:
                return b

# return ordered set for B_curl(a,b)
# where a is the dimension of the tuple, and k is the sum
def B_curl(n, k):
    tmp = B_curl_h(n, k)
    return list(map(tuple, tmp))

def B_curl_h(n, k):
    if n == 1:
        return [[k]]

    if k == 0:
        return fp.lmap(lambda xs: addhd(0, xs), B_curl_h(n - 1, 0))
    
    # for each possible value, get one
    res = []
    for i in range(k + 1):
        res += fp.lmap(lambda xs: addhd(i, xs), B_curl_h(n - 1, k - i))

    return res

# the number of elements in B_curl
def B_curl_num(n, k):
    if n == 1:
        return 1

    if k == 0:
        return 1
    
    res = 0
    for i in range(k + 1):
        res += B_curl_num(n - 1, k - i)

    return res

# return ordered set for A_curl(a,b)
def A_curl(n, k):
    res = []
    for k0 in range(k + 1):
        res += B_curl(n, k0)

    return res

# return ordered set for A_curl(a,b)
def A_curl_num(n, k):
    res = 0
    for k0 in range(k + 1):
        res += B_curl_num(n, k0)

    return res

# function to fast add head to a list
def addhd(hd, xs):
    xs.insert(0, hd)
    return xs

#def ncr(n, r):
#    r = min(r, n-r)
#    numer = reduce(op.mul, range(n, n-r, -1), 1)
#    denom = reduce(op.mul, range(1, r+1), 1)
#    return numer / denom

# calc n choose multiindex rs

def ncrs(n, rs):
    res = factorial(n)
    r_sum = 0
    for r in rs:
        res = res / factorial(r)
        r_sum = r_sum + r

    return res / factorial(n - r_sum)

# search symetric tuples
#def get(mydict, key):
#    if key[0] > key[1]:
#        return mydict[key[1], key[0], key[2], key[3]]
#    else:
#        return mydict[key]


# rationalize input
def rat(val, rational):
    if rational is False:
        return float(val)
    else:
        return Rational(val)


if __name__ == '__main__':
    from sympy.plotting import plot
    
    plot(eta(1, oo, x), (x, -1, 5))

# load serialized formulas
# stat from enums
def load_formulas(gname, phiname, stat, folder='./.formulas/'):
    path = folder + gname + '_' + phiname + '_' + str(stat) + '.sav'
    dill.load(open(path, 'rb'))
    try:
        return dill.load(open(path, 'rb'))
    except:
        return None

# get largets components
def get_largest_component(g, save=True):
    if nx.is_connected(g):
        return g
    else:
        g = g.subgraph(max(nx.connected_components(g), key=len))
        prob_rescale(g, 'x')
        prob_rescale(g, 'y')
        if save:
            output = []
            head = ['i', 'j', 'l', 'x', 'y']
            output.append(head)
            for e in g.edges():
                erow = []
                e0 = min(int(e[0]), int(e[1]))
                e1 = max(int(e[0]), int(e[1]))
                erow.append(e0)
                erow.append(e1)
                erow.append(float(g.edges[e]['l']))
                erow.append(float(g.edges[e]['x']))
                erow.append(float(g.edges[e]['y']))
                output.append(erow)
            tw.tableWrite(output, './' + g.name + '_cc.dat', formatType='n')

        return g

# rescale prob
def prob_rescale(g, prop):
    tot = 0.0
    for e in g.edges():
        tot += g.edges[e][prop]
    for e in g.edges():
        g.edges[e][prop] = g.edges[e][prop] / tot

# check basic info of g
def gcheck(g, eps=1e-7):
    # is connected
    is_con = is_connected(g)
    # is p_x add up to 1
    px_tot = 0
    py_tot = 0
    # tolorence
    for e in g.edges():
        px_tot += g.edges[e]['x']
        py_tot += g.edges[e]['y']

    if abs(px_tot - 1) < eps:
        px_one = True
    else:
        px_one = False

    if abs(py_tot - 1) < eps:
        py_one = True
    else:
        py_one = False

    return {'connected': is_con, 
            'px_one': (px_one, float(px_tot)), 
            'py_one': (py_one, float(py_tot)),
            'total': (is_con and px_one and py_one)}




