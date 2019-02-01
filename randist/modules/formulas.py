from . import commonFuncs as cf
from . import numericFuncs as nf
from . import basicInfo as bi
from .pyprelude.Timer import Timer
from .pyprelude.Progress import Progress
from .pyprelude import EasyWriter as ew
from .enums import Stats
from sympy import symbols, lambdify
from sympy.abc import x, p, q
from .serializedFormula import *
from .plot import plot1d
from .pyprelude.Memorization import memorize
import os
import dill


# template for all region-wise operations
class Formula:
    def __init__(self, g, memorize):
        self.g = g
        self.stat = None
        self.keys = None
        self.unikey = None
        self.idx_num = 0
        self.val_keys = None
        self.resfolder = './results/'
        self.plot_info = [None, x, -0.1, None]  # plotting parameters
        self.memo = memorize
        self.memo_dict()

    # set up the symbolic or numeric environment
    def sym_num_env(self, symbolic):
        self.symbolic = symbolic
        g = self.g
        if symbolic:
            # assgin symbolic functions
            from .Sregions import get_R, get_L, get_q
            from .commonFuncs import eta, etal, etar
            self.get_R = get_R
            self.get_L = get_L
            self.get_q = get_q
            self.eta = eta
            self.etal = etal
            self.etar = etar
            
            # assign symbolic phis
            g.phi_p = g.phi.phi_p_S
            g.phi_q = g.phi.phi_q_S
            g.phi_pq = g.phi.phi_pq_S
            g.phi_qcp = g.phi.phi_qcp_S

            # set extra properties
            self.fs = {} # all formulas
            self.N_fs = {} # all numeric formulas
            self.unikey = 'zero'
            self.mods = ['numpy', {'theta': nf.theta, 'eta': nf.eta, 'etal': nf.etal, 'etar': nf.etar, 'mmin': min, 'mmax': max}]  ## modules for lambdify
            self.folder = './.formulas/'
            self.mksvname()

        else:
            # assgin symbolic functions
            from .Nregions import get_R, get_L, get_q
            from .numericFuncs import eta, etal, etar
            self.get_R = get_R
            self.get_L = get_L
            self.get_q = get_q
            self.eta = eta
            self.etal = etal
            self.etar = etar
            
            # assign symbolic phis
            g.phi_p = g.phi.phi_p_N
            g.phi_q = g.phi.phi_q_N
            g.phi_pq = g.phi.phi_pq_N
            g.phi_qcp = g.phi.phi_qcp_N

    def memo_dict(self):
        self.dict_coeff = {}

    def cond_ep(self, g, k, e, p_val, x_val, alphas, prog):
        res = 0
        # get e related info
        le = float(g.edges[e]['l'])
        px = float(g.edges[e]['x'])
        for f in g.edges():

            prog.count()

            # get f related info
            lf = float(g.edges[f]['l'])
            py = float(g.edges[f]['y'])
            # get entry ef related info
            d, p1, p2, q1, q2 = memorize(self.g.dict_entry, (e, f), bi.entry_info,(self.g, e, f, le, lf), on=self.memo)
            #d, p1, p2, q1, q2 = bi.entry_info(self.g, e, f, le, lf)

            # get entry coeff
            coeff = memorize(self.dict_coeff, (e, f), self.ef_coeff, (px, py, lf), on=self.memo)
            #coeff = self.ef_coeff(px, py, lf)
            ef_res = 0

            for (i, j) in g.two2:
                # get region related info
                R = self.get_R(g, e, f, i, j, le, lf, d, p1, p2, q1, q2, x_val)
                ef_res += self.region_op(g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas)

            res += coeff * ef_res
        return res

    def cond_region(self, k=None, e=None, p_val=None, x_val=None, show=True):
        # generate extra params
        alphas = None
        if self.stat == Stats.MOMENT or self.stat == Stats.CMOMENT:
            alphas = cf.A_curl(2, k)

        g = self.g
        res = 0

        if show:
            print('computing', g.name, g.phi.name, str(self.stat)+'...')


        # treat conditional
        if e is not None:
            # see progress
            prog = Progress(g.number_of_edges(), label='computing', response_time=60)
            return self.cond_ep(g, k, e, p_val, x_val, alphas, prog)

        # see progress
        prog = Progress(g.number_of_edges() ** 2, response_time=60)

        for e in g.edges():
            res += self.cond_ep(g, k, e, p_val, x_val, alphas, prog)
        return res
    
    # combine results in e,f level
    def ef_coeff(self, px, py, lf):
        if self.stat == Stats.MOMENT:
            coeff = 1
        elif self.stat == Stats.CDF:
            coeff = px * py
        elif self.stat == Stats.PDF:
            coeff = px * py / lf
        elif self.stat == Stats.CMOMENT:
            coeff = 1
        elif self.stat == Stats.CCDF:
            coeff = py
        elif self.stat == Stats.CPDF:
            coeff = py / lf
        return coeff

    # save result when evaluate
    def save_res(self, keys, res):
        g = self.g
        fname = self.resfolder + g.name + '_' + g.phi.name + '_' + str(self.stat) + '.dat'
        val = str(keys) + '\t' + str(res) + '\n'
        ew.wFile(fname, val)

    # make save name
    def mksvname(self):
        self.fullsave = self.folder + self.g.name + '_' + self.g.phi.name + '_' + str(self.stat) + '.sav'

    # make dict from input
    def make_params(self, *params):
        p_dict = {}
        val_dict = {}
        keys = []
        vals = []
        for idx, v in enumerate(params):
            if idx < len(self.keys):
                if self.keys[idx] == 'p_val':
                    # use limits instead of undefined p value
                    v = self.adj_p_val(v)
                    val_dict['p_val'] = v
                    vals.append(v)
                    if self.symbolic:
                        p_dict['p_val'] = p
                    else:
                        p_dict['p_val'] = v
                elif self.keys[idx] == 'x_val':
                    val_dict['x_val'] = v
                    vals.append(v)
                    if self.symbolic:
                        p_dict['x_val'] = x
                    else:
                        p_dict['x_val'] = v
                else:
                    keys.append(v)
                    p_dict[self.keys[idx]] = v
            else:
                break

        if keys == []:
            keys = [self.unikey]

        keys = tuple(keys)
        vals = tuple(vals)

        return p_dict, val_dict, keys, vals

    # use limit to replace undefined p
    def adj_p_val(self, p_val, eps=1e-7):
        if p_val > 0 and p_val < 1:
            return p_val
        elif p_val == 0:
            return eps
        elif p_val == 1:
            return 1 - eps
        else:
            raise Exception('p_val has to be in [0, 1]')

    ### abstract methods
    # operations in each region
    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        pass


class Moment(Formula):
    def __init__(self, g, symbolic, memorize):
        super().__init__(g, memorize)
        self.moment_info = {}
        self.symbolic = symbolic
        self.stat = Stats.MOMENT
        self.idx_num = 1
        self.keys = ['k']
        self.sym_num_env(symbolic)

    def get_func(self, g, alpha):
        if self.symbolic:
            p, q = symbols('p,q')
            func = q ** alpha[0] * p ** alpha[1] * g.phi_pq
        else:
            func = lambda q, p: q ** alpha[0] * p ** alpha[1] * g.phi_pq(q, p)
        return func

    def get_const(self, g, e, f, i, j, le, lf, px, py, R, alpha):
        c0 = px * py * lf ** alpha[0] * le ** alpha[1]
        if e == f:
            w = (i + j + 1) * alpha[0] + (i + j + 2) * alpha[1]
            c1 = (-1) ** w 
        else:
            w = j * alpha[0] + i * alpha[1]
            c1 = (-1) ** w 
        c = c0 * c1
        func = self.get_func(g, alpha)

        m = R.m(func)
        return c * m


    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        res = 0
        # get alpha related info
        for alpha in alphas:
            #if (e, f, i, j, alpha) not in g.moment_info:
            #c0 = px * py * lf ** alpha[0] * le ** alpha[1]
            #if e == f:
            #    w = (i + j + 1) * alpha[0] + (i + j + 2) * alpha[1]
            #    c1 = (-1) ** w 
            #else:
            #    w = j * alpha[0] + i * alpha[1]
            #    c1 = (-1) ** w 
            #c = c0 * c1
            #func = self.get_func(g, alpha)

            #m = R.m(func)

            const = memorize(
                    self.moment_info, 
                    (e, f, i, j, alpha), 
                    self.get_const, 
                    (g, e, f, i, j, le, lf, px, py, R, alpha),
                    on=self.memo
                    )

            if e == f:
                c2 = cf.ncrs(k, alpha) * (i * (d + le)) ** (k - alpha[0] - alpha[1])
            else:
                c2 = cf.ncrs(k, alpha) * (d[i, j] + i * le + j * lf) ** (k - alpha[0] - alpha[1])

            res += c2 * const
        return res


class CDF(Formula):
    def __init__(self, g, symbolic, memorize):
        super().__init__(g, memorize)
        self.stat = Stats.CDF
        self.symbolic = symbolic
        self.keys = ['x_val']
        self.val_keys = (x,)
        self.sym_num_env(symbolic)
        self.stop_val = 1

    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        return R.m(g.phi_pq)


class PDF(Formula):
    def __init__(self, g, symbolic, memorize):
        super().__init__(g, memorize)
        self.stat = Stats.PDF
        self.symbolic = symbolic
        self.keys = ['x_val']
        self.val_keys = (x,)
        self.sym_num_env(symbolic)
        self.stop_val = 0

    def get_func(self, q_func, g):
        if self.symbolic:
            p, q = symbols('p,q')
            func = g.phi_pq.subs(q, q_func)
        else:
            func = lambda p: g.phi_pq(q_func(p), p)
        return func

    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        c = self.eta(R.a_val, R.b_val, x_val)
        L = self.get_L(g, e, f, i, j, le, lf, d, p1, p2, q1, q2, x_val)
        q_func = self.get_q(g, e, f, i, j, le, lf, d, p1, p2, q1, q2, x_val)
        phis = self.get_func(q_func, g)
        m = L.m(phis)
        return c * m


class CMoment(Formula):
    def __init__(self, g, symbolic, memorize):
        super().__init__(g, memorize)
        self.stat = Stats.CMOMENT
        self.symbolic = symbolic
        self.idx_num = 2
        self.keys = ['k', 'e', 'p_val']
        self.val_keys = (p,)
        self.sym_num_env(symbolic)
        self.plot_info = [None, p, 0, 1]
        self.stop_val = 0

    def get_func(self, g, p_val, alpha):
        if self.symbolic:
            p, q = symbols('p,q')
            func = q ** alpha[0] * g.phi_qcp
        else:
            func = lambda q: q ** alpha[0] * g.phi_qcp(q, p_val)
        return func

    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        res = 0
        for alpha in alphas:
            c0 = cf.ncrs(k, alpha) * py * lf ** alpha[0] * le ** alpha[1]
            if e == f:
                w = (i + j + 1) * alpha[0] + (i + j + 2) * alpha[1]
                c1 = (-1) ** w * (i * (d + le)) ** (k - alpha[0] - alpha[1])
            else:
                w = j * alpha[0] + i * alpha[1]
                c1 = (-1) ** w * (d[i, j] + i * le + j * lf) ** (k - alpha[0] - alpha[1])
            c = c0 * c1 * p_val ** alpha[1]

            func = self.get_func(g, p_val, alpha)

            m = R.m_p(func, p_val)
            res += c * m

        return res


class CCDF(Formula):
    def __init__(self, g, symbolic, memorize):
        super().__init__(g, memorize)
        self.stat = Stats.CCDF
        self.symbolic = symbolic
        self.idx_num = 1
        self.keys = ['e', 'p_val', 'x_val']
        self.val_keys = (p, x)
        self.sym_num_env(symbolic)
        self.stop_val = 1

    def get_func(self, g, p_val):
        if self.symbolic:
            p, q = symbols('p,q')
            func = g.phi_qcp
        else:
            func = lambda q: g.phi_qcp(q, p_val)
        return func

    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        func = self.get_func(g, p_val)
        return R.m_p(func, p_val)


class CPDF(Formula):
    def __init__(self, g, symbolic, memorize):
        super().__init__(g, memorize)
        self.stat = Stats.CPDF
        self.symbolic = symbolic
        self.idx_num = 1
        self.keys = ['e', 'p_val', 'x_val']
        self.val_keys = (p, x)
        self.sym_num_env(symbolic)
        self.stop_val = 0

    def get_func(self, g, q_func, p_val):
        if self.symbolic:
            func = g.phi_qcp.subs(q, q_func)
        else:
            func = g.phi_qcp(q_func(p_val), p_val)
        return func

    def region_op(self, g, e, f, i, j, le, lf, px, py, d, p1, p2, q1, q2, R, p_val, x_val, k, alphas):
        c0 = self.eta(R.a_val, R.b_val, x_val)
        L = self.get_L(g, e, f, i, j, le, lf, d, p1, p2, q1, q2, x_val)
        q_func = self.get_q(g, e, f, i, j, le, lf, d, p1, p2, q1, q2, x_val)
        myeta = None
        if L.bd[0] is False:
            myeta = self.etal
        elif L.bd[1] is False:
            myeta = self.etar
        else:
            myeta = self.eta
        c1 = myeta(L.pl, L.pu, p_val)
        phis = self.get_func(g, q_func, p_val)
        return c0 * c1 * phis


# the interface for numerical computation
class Numeric:
    # fl_cls is the formula class, e.g. Moment, CDF, CMoment, etc.
    def __init__(self, g, fl_cls, memorize=False):
        # gen formula
        self.fm = fl_cls(g, False, memorize=memorize)

    # evaluate value
    def eval(self, *params, save=True):
        fm = self.fm
        p_dict, v_dict, keys, vals = fm.make_params(*params)
        res = fm.cond_region(**p_dict)
        if save:
            fm.save_res(params, res)
        return res

    # numerical plot
    def plot(self, *params, pnts=1000, save=True, show=False):
        fm = self.fm
        if fm.stat == Stats.MOMENT:
            return 0
        p_dict, v_dict, keys, vals = fm.make_params(*params)
        x_key = fm.keys[len(fm.keys)-1]

        def f_lambda(x):
            p_dict[x_key] = x
            return fm.cond_region(show=False, **p_dict)
        
        var = fm.plot_info[1]
        lb = fm.plot_info[2]
        ub = fm.plot_info[3]

        # get upper bound
        if ub is None:
            print('updating plotting bounds...')
            if fm.g.d_max > 0:
                ub = fm.g.d_max
                adaptive = False
            elif fm.g.jit and 'e' in fm.keys:
                tmpe = p_dict['e']
                bi.get_d_jit(fm.g, tmpe[0], tmpe[1], tmpe)
                ub = fm.g.de_max[tmpe]
                adaptive = True
            else:
                ub = fm.g.dd_max
                adaptive = True
        else:
            adaptive = False

        step = ub / float(pnts)
        g = fm.g
        print('plotting', g.name, g.phi.name, str(fm.stat)+'...')

        if save:
            g = fm.g
            figname = fm.resfolder + g.name + '_' + g.phi.name + '_' + str(fm.stat) + '_' + str(params) + '.png'
            plot1d(f_lambda, lb, ub, step, svname=figname, show=show, stop_val=fm.stop_val, adaptive=adaptive)
        else:
            plot1d(f_lambda, lb, ub, step, show=show, stop_val=fm.stop_val, adaptive=adaptive)


# the interface for symbolic computation
class Symbolic:
    # fl_cls is the formula class, e.g. Moment, CDF, CMoment, etc.
    def __init__(self, g, fl_cls, memorize=False):

        # gen formula
        self.fm = fl_cls(g, True, memorize=memorize)

    # generate functions
    def gen_formula(self, *params):
        fm = self.fm
        p_dict, v_dict, keys, vals = fm.make_params(*params)
        p_dict = self.add_default_var(p_dict)
        if keys not in fm.fs:
            expr = fm.cond_region(**p_dict)
            if fm.plot_info[3] is None:
                fm.plot_info[3] = fm.g.d_max + 1
            fm.fs[keys] = expr
            if fm.val_keys is None:
                fm.N_fs[keys] = expr
            else:
                fm.N_fs[keys] = lambdify(fm.val_keys, expr, modules=fm.mods)
        return v_dict, keys, vals, fm.fs[keys], fm.N_fs[keys]

    # add default
    def add_default_var(self, p_dict):
        fm = self.fm
        if 'x_val' in fm.keys and 'x_val' not in p_dict:
            p_dict['x_val'] = x
        if 'p_val' in fm.keys and 'p_val' not in p_dict:
            p_dict['p_val'] = p
        return p_dict

    # plot formulas
    def plot(self, *params, step=0.01, save=True, show=False):
        fm = self.fm
        if fm.stat == Stats.MOMENT:
            return 0

        v_dict, keys, vals, f, N_f = self.gen_formula(*params)
        my_f = self.partial_apply(v_dict, f)

        var = fm.plot_info[1]
        lb = fm.plot_info[2]
        ub = fm.plot_info[3]

        f_lambda = lambdify(var, my_f, modules=fm.mods)

        if save:
            g = fm.g
            figname = fm.resfolder + g.name + '_' + g.phi.name + '_' + str(fm.stat) + '_' + str(params) + '.png'
            plot1d(f_lambda, lb, ub, step, svname=figname, show=show)
        else:
            plot1d(f_lambda, lb, ub, step, show=show)

    # evaluate value
    def eval(self, *params, save=True):
        fm = self.fm
        v_dict, keys, vals, f, N_f = self.gen_formula(*params)
        if len(vals) == 0:
            res = N_f
        else:
            res = N_f(*vals)
        if save:
            fm.save_res(params, res)
        return res

    # make sublist
    def make_sub_lst(self, v_dict):
        subval = []
        if 'x_val' in v_dict:
            subval.append((x, v_dict['x_val']))

        if 'p_val' in v_dict:
            subval.append((p, v_dict['p_val']))
        return subval

    # print formula
    def formula(self, *params):
        fm = self.fm
        v_dict, keys, vals, f, N_f = self.gen_formula(*params)
        return self.partial_apply(v_dict, f)

    # partial apply
    def partial_apply(self, v_dict, f):
        subval = self.make_sub_lst(v_dict)
        if len(subval) == 0:
            return f
        else:
            return f.subs(subval)

    # save formulas
    def save_formulas(self):
        fm = self.fm
        sf = SFormula()
        sf.stat = fm.stat
        sf.fs = fm.fs
        sf.N_fs = fm.N_fs
        sf.mods = fm.mods
        sf.idx_num = fm.idx_num
        sf.val_keys = fm.val_keys
        sf.plot_info = fm.plot_info
        sf.unikey = fm.unikey

        # create folder
        if not os.path.exists(fm.folder):
            os.makedirs(fm.folder)

        # pickle sf
        dill.settings['recurse'] = True
        dill.dump(sf, open(fm.fullsave, 'wb'))

        return sf

# the wrapper for getting formulas
class Formulas:
    # symbolic: use symbolic or numerical method, None is same as auto
    def __init__(self, gname, phi, fpath='../data/', rational=False, d_jit=False, memorize=True):
        self.d_jit = d_jit
        self.memo = memorize
        # read graph
        self.g = bi.readGraph(fpath, gname)
        # generate basic info
        bi.basicInfo(self.g, phi, rational, d_jit)
        # dispatch map
        self.fl = {
                Stats.MOMENT: Moment,
                Stats.CDF: CDF,
                Stats.PDF: PDF,
                Stats.CMOMENT: CMoment,
                Stats.CCDF: CCDF,
                Stats.CPDF: CPDF
                }
        # conditional names
        self.condi = [
                Stats.CMOMENT,
                Stats.CCDF,
                Stats.CPDF
                ]

    # get different stats
    def get_formula(self, stats, symbolic=None):
        g = self.g
        if Stats.is_member(stats) is False:
            raise Exception('stats must be value from the enum Stats')

        if symbolic is None:
            if stats == Stats.MOMENT or stats == Stats.CMOMENT:
                symbolic = False
            else:
                symbolic = True

        if symbolic:
            return Symbolic(g, self.fl[stats], self.memo)
        else:
            return Numeric(g, self.fl[stats], self.memo)
