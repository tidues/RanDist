import networkx as nx
from .pyprelude import GraphGen as gg
from .commonFuncs import *
from sympy import *
import time


# reads a graph input file
def readGraph(fpath, gname):
    print('loading graph...')
    g = gg.GraphFromFile(fpath, gname).G
    g.name = gname
    return g

def basicInfo(g, phi, rational=False, d_jit=False):
    print('generating basic info...')
    g.rat = rational
    g.phi = phi

    # check graph info
    check_res = gcheck(g)
    if check_res['total'] is not True:
        raise Exception('Input did not pass all test: ', check_res)

    # dicts for global memorization
    g.dict_entry = {}

    # index set
    g.two = (0,1)
    g.two2 = [(i, j) for i in g.two for j in g.two]
    end = time.time()
    
    # get max edge length
    g.max_l = 0
    for e in g.edges():
        if g.edges[e]['l'] > g.max_l:
            g.max_l = g.edges[e]['l'] 

    g.d_max = -1
    g.dd_max = -1
    g.de_max = {}

    g.d = {}
    if d_jit is False:
        get_d(g)
        g.jit = False
    else:
        g.jit = True




# entry info
def entry_info(g, e, f, le, lf):
    p1 = None
    p2 = None
    q1 = None
    q2 = None
    if e == f:
        if g.jit is False:
            d = g.d[e[0]][e[1]]
        else:
            d = get_d_jit(g, e[0], e[1], e)
    else:
        d = {}
        if g.jit is False:
            for (i, j) in g.two2:
                d[i, j] = g.d[e[i]][f[j]]
        else:
            for (i, j) in g.two2:
                d[i, j] = get_d_jit(g, e[i], f[j], e)
        p1 = (-d[0, 0] + d[1, 0] + le) / (2 * le)
        p2 = (-d[0, 1] + d[1, 1] + le) / (2 * le)
        q1 = (-d[0, 0] + d[0, 1] + lf) / (2 * lf)
        q2 = (-d[1, 0] + d[1, 1] + lf) / (2 * lf)

    return(d, p1, p2, q1, q2)

# get d value just in time
def get_d_jit(g, u, v, e):
    if u in g.d:
        return g.d[u][v]
    elif v in g.d:
        return g.d[v][u]
    else:
        get_d(g, mye=e) 
        return g.d[u][v]


#########################################################################
# help functions                                                        #
#########################################################################

# get shortest path matrix D
def get_d(g, mye=None):
    if mye is None:
        print("loading all pairs shortest length...")
        g.d = dict(nx.shortest_path_length(g, weight = 'l'))
        update_dd_max(g)
    else:
        print("loading shortest length to nodes of edge", str(mye)+"...")
        g.d[mye[0]] = nx.shortest_path_length(g, source=mye[0], weight='l')
        g.d[mye[1]] = nx.shortest_path_length(g, source=mye[1], weight='l')
        update_dd_max(g, mye)

    # if g.rat:
    #     for i in g.nodes():
    #         for j in g.nodes():
    #             g.d[i][j] = rat(g.d[i][j], g.rat)

# update d_max
def update_dd_max(g, e=None):
    if e is None:
        if g.dd_max < 0:
            for i in g.nodes():
                for j in g.nodes():
                    if i < j:
                        if g.d[i][j] > g.dd_max:
                            g.dd_max = g.d[i][j]
            g.dd_max += g.max_l
    else:
        if e not in g.de_max:
            de_max = 0
            for j in g.d[e[0]]:
                if g.d[e[0]][j] > de_max:
                    de_max = g.d[e[0]][j]
            g.de_max[e] = de_max + g.edges[e]['l']






