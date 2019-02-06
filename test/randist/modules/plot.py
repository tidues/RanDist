import numpy as np
import matplotlib.pyplot as plt
from .pyprelude import FPToolBox as fp
from .pyprelude.Progress import Progress

def plot1d(func, lb, ub, step, stop_val=None, stop_iter=50, svname='', show=False, esp=1e-7, adaptive=False):
    x = np.arange(lb, ub, step)
    prog = Progress(len(x), label='plotting', response_time=60)
    if adaptive:
        y = []
        stop_cnt = 0
        for xval in x:
            prog.count()
            yval = func(xval)
            y.append(yval)
            if abs(yval - stop_val) < esp:
                stop_cnt += 1
                if stop_cnt > stop_iter:
                    break
            else:
                stop_cnt = 0
        x = x[:len(y)]
    else:
        y = fp.lmap(func, x)

    fig = plt.figure(1)
    plt.minorticks_off()
    plt.plot(x, y, 'k', color='b')
    if svname != '':
        plt.savefig(svname)
    if show:
        plt.show()
    plt.close(fig)

#def find_ub(func, lb, step, lim, nochange_iter=6, eps=1e-6):
#    ub = lb
#    power = 0
#    y0 = func(ub)
#    while True:
#        ub += step * (2 ** power)
#        print(ub)
#        if ub > lim:
#            return ub
#
#        y1 = func(ub)
#        if abs(y0-y1) < eps:
#            if power > nochange_iter:
#                return ub
#            else:
#                y0 = y1
#                power += 1
#        else:
#            y0 = y1
#            power = 0
#


        

