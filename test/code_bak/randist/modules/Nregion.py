from scipy.integrate import quad, dblquad
from . import numericFuncs as nf
import math

# basic components of a region
class RegionBase:
    def __init__(self, pl, pu, ql, qu, xval, bd=(True, True)):
        self.pl = pl
        self.pu = pu
        self.ql = ql
        self.qu = qu
        self.xval = xval # is x if it is a region function; or upper bound if is a region
        self.bd = bd
        # self.modules = ['numpy']

    # the mass function
    def m(self, func):
        if self.ql is None:
            region = (self.pl, self.pu)
            int_func = quad
        else:
            int_func = dblquad
            region = (self.pl, self.pu, self.ql, self.qu)

        return int_func(func, *region)[0]

    # conditional mass function
    def m_p(self, f, p_val):
        myeta = None
        if self.bd[0] is False:
            myeta = nf.etal
        elif self.bd[1] is False:
            myeta = nf.etar
        else:
            myeta = nf.eta

        etaval = myeta(self.pl, self.pu, p_val)
        if etaval != 0:
            return quad(f, self.ql(p_val), self.qu(p_val))[0]
        else:
            return 0

    # print region description
    def print(self):
        print('pl:\t', self.pl)
        print('pu:\t', self.pu)
        print('ql:\t', self.ql)
        print('qu:\t', self.qu)
        print('xval:\t', self.xval)

