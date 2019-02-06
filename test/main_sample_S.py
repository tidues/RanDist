from sympy.abc import x, p, q
import randist as rt

Stats = rt.Stats
load_formulas = rt.load_formulas
pdf_check = rt.pdf_check


# module test switch
switches = {
        Stats.MOMENT: 1,
        Stats.CDF: 1,
        Stats.PDF: 1,
        Stats.CMOMENT: 1,
        Stats.CCDF: 1,
        Stats.CPDF: 1
        }

show_plot = False

#if switches[Stats.SAVE] == 1:
#    moment = load_formulas(Stats.MOMENT)
#    print(moment.stat)
#    print(moment.eval(0))
#    print(moment.eval(1))
#    print(moment.eval(2))
#    cdf = load_formulas(Stats.CDF)
#    cdf.plot()

# graph file
gname = 'g0'
phi_pq = 1
phi_pq = 6 * q * (1 - q)
phi = rt.Phi('betaq', phi_pq=phi_pq)

# formulas class
fls = rt.Formulas(gname, phi)

# test values
valLst = [-0.1, -0.01, -0.001, 0, 1, 2, 3, -1, 9, 9.5, 9.9, 10]

## simulation 
#if switches[Stats.SIMULATION] == 1:
#    sim = sl.events(g)
#    print(sim.E_d(f=lambda x: x**3))

# moments stats
if switches[Stats.MOMENT] == 1:
    moment = fls.get_formula(Stats.MOMENT, symbolic=True)
    vals = [0, 1, 2, 3]
    for v in vals:
        print(moment.eval(v))

# cdf stats
if switches[Stats.CDF] == 1:
    cdf = fls.get_formula(Stats.CDF)
    #vals = [0, 0.5, 1, 3, 5]
    #for v in vals:
    #    print(cdf.eval(v))
    #cdf.formula()
    cdf.plot(show=show_plot)
    #cdf.save_formulas()
    #mcdf = load_formulas(gname, phi.name, Stats.CDF)
    #cdf.plot(show=True)
    

# pdf stats
if switches[Stats.PDF] == 1:
    pdf = fls.get_formula(Stats.PDF)
    #f = pdf.formula()
    #print(pdf_check(f, (x, 0, 12)))
    pdf.plot(show=show_plot)
    #for x_val in valLst:
    #    print(x_val, '\t', pdf.eval(x_val))

# conditional moments stats
if switches[Stats.CMOMENT] == 1:
    ks = [0, 1, 2]
    es = [('1', '2')]
    ps = [0, 0.5, 1]
    cmoment = fls.get_formula(Stats.CMOMENT, symbolic=True)

    for k in ks:
        for e in es:
            for p in ps:
                print(cmoment.eval(k, e, p))

    cmoment.plot(0, ('1', '2'), show=False)
    cmoment.plot(1, ('1', '2'), show=False)
    cmoment.plot(2, ('1', '2'), show=False)


# conditional cdf
if switches[Stats.CCDF] == 1:
    ccdf = fls.get_formula(Stats.CCDF)
    es = [('1', '2')]
    ps = [0, 0.5, 1]
    xs = [0, 0.5, 1, 3, 5]

    for e in es:
        for p in ps:
        #    for x in xs:
        #        print(ccdf.eval(e, p, x))
            ccdf.plot(e, p, show=show_plot)
    #e = ('1', '2')
    #ccdf.plot(e, 0, show=True)
    #ccdf.plot(e, 0.2, show=True)
    #ccdf.plot(e, 0.4, show=True)
    #ccdf.plot(e, 0.5, show=True)
    #ccdf.plot(e, 0.8, show=True)
    #ccdf.plot(e, 1, show=True)

# conditional pdf
if switches[Stats.CPDF] == 1:
    cpdf = fls.get_formula(Stats.CPDF)
    e = ('1', '2')
    ps = [0, 0.2, 0.4, 0.5, 0.8, 1]
    x = 3

    for p in ps:
        #print(cpdf.eval(e, p, x))
        cpdf.plot(e, p, show=show_plot)
        #print(pdf_check(cpdf.formula(e, p), (x, 0, g.d_max)))


# time comparison
# take an region
#if switches[Stats.TIMING] == 1:
#    e = ('1', '2')
#    f = ('3', '4')
#    mods = ['numpy', {'theta': nf.theta, 'eta': nf.eta, 'etal': nf.etal, 'etar': nf.etar}]
#
## symbolic integration
#    # flow1: symbolic -> sum -> lambdify -> evaluation
#    # symbolic + sum
#    print('starting flow 1')
#    start = time.time()
#    expr = 0
#    for t in range(1000):
#        for (i, j) in g.two2:
#            expr += g.Rx[e, f, i, j].m(phi_pq)
#    end = time.time()
#    f1sym = end - start
#    
#    # lambdify
#    start = time.time()
#    expr = expand(expr)
#    myf = lambdify(x, expr, modules=mods)
#    end = time.time()
#    f1lbd = end - start
#
#    # evaluation
#    start = time.time()
#    val1 = 0
#    for x_val in np.arange(4, 5, 1):
#        val1 += myf(x_val)
#    end = time.time()
#    f1eval = end - start
#    res1 = [('sym', f1sym), ('lbd', f1lbd), ('eval', f1eval)]
#
#    
#    # flow2: symbolic -> lambdify -> evaluation -> sum
#    # symbolic + lambdify
#    #start = time.time()
#    #myf = {}
#    #for t in range(1):
#    #    for (i, j) in g.two2:
#    #        myf[i, j, t] = lambdify(x, g.Rx[e, f, i, j].m(phi_pq), mods)
#    #end = time.time()
#    #f2sym = end - start
#
#    ## evaluation + sum
#    #start = time.time()
#    #val2 = 0
#    #for x_val in np.arange(0, 5, 0.001):
#    #    for t in range(1):
#    #        for (i, j) in g.two2:
#    #            val2 += myf[i, j, t](x_val)
#    #end = time.time()
#    #f2eval = end - start
#    #
#    #res2 = [('sym', f2sym), ('eval', f2eval)]
#
#    # flow3: numerical integration
#    # symbolic + sum
#    print('starting flow 3')
#    start = time.time()
#    val3 = 0
#    for x_val in np.arange(4, 5, 1):
#        for t in range(1000):
#            for (i, j) in g.two2:
#                val3 += g.Rx[e, f, i, j].m_num(phi_pq, x_val)
#    end = time.time()
#    eval3 = end - start
#
#    print('val1:\t', val1)
#    # print('val2:\t', val2)
#    print('val2:\t', val3)
#    print('\nflow1:')
#    total = 0
#    for it in res1:
#        total += it[1]
#        print(it[0], ':\t', it[1])
#    print('total:\t', total)
#    #print('\nflow2:')
#    #total = 0
#    #for it in res2:
#    #    total += it[1]
#    #    print(it[0], ':\t', it[1])
#    #print('total:\t', total)
#    print('\nflow3:')
#    print('total:\t', eval3)
