import randist as rt
from sympy.abc import p, q
# from commonFuncs import gcheck
Stats = rt.Stats


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

# graph file
gname = 'g0'

#phi_pq = 4 * p * q
phi_pq = 6 * q * (1 - q)
#phi_pq = 1
phi = rt.Phi('betaq', phi_pq=phi_pq)

fls = rt.Formulas(gname, phi, memorize=True)

# test values
valLst = [-0.1, -0.01, -0.001, 0, 1, 2, 3, -1, 9, 9.5, 9.9, 10]

# moments stats
if switches[Stats.MOMENT] == 1:
    moment = fls.get_formula(Stats.MOMENT)
    vals = [0, 1, 2, 3]
    for v in vals:
        #print(moment.eval(v))
        print(moment.X_coeff(k_val=v))
        print(moment.Y_coeff(k_val=v))

# cdf stats
if switches[Stats.CDF] == 1:
    cdf = fls.get_formula(Stats.CDF, symbolic=False)
    #vals = [0, 0.5, 1, 3, 5]
    #for v in vals:
    #    print(cdf.eval(v))
    #cdf.plot(show=show_plot)
    print(cdf.X_coeff(x_val=3))
    print(cdf.Y_coeff(x_val=3))

# pdf stats
if switches[Stats.PDF] == 1:
    pdf = fls.get_formula(Stats.PDF, symbolic=False)
    #for x_val in valLst:
    #    print(x_val, '\t', pdf.eval(x_val))
    #pdf.plot(show=show_plot)
    print(pdf.X_coeff(x_val=3))
    print(cdf.Y_coeff(x_val=3))

# conditional moments stats
if switches[Stats.CMOMENT] == 1:
    cmoment = fls.get_formula(Stats.CMOMENT)
    ks = [0, 1, 2]
    es = [('1', '2')]
    ps = [0, 0.5, 1]

    for k in ks:
        for e in es:
            for p in ps:
                print(cmoment.eval(k, e, p))
                print(cmoment.Y_coeff_condi(e, p, k_val=k))
            #cmoment.plot(k, e, show=show_plot)

# conditional cdf stats
if switches[Stats.CCDF] == 1:
    ccdf = fls.get_formula(Stats.CCDF, symbolic=False)
    es = [('1', '2')]
    ps = [0, 0.5, 1]
    xs = [0, 0.5, 1, 3, 5]

    for e in es:
        for p in ps:
            for x in xs:
                print(ccdf.Y_coeff_condi(e, p, x_val=x))
    #            print(ccdf.eval(e, p, x))
            #ccdf.plot(e, p, show=show_plot)

# conditional pdf stats
if switches[Stats.CPDF] == 1:
    cpdf = fls.get_formula(Stats.CPDF, symbolic=False)
    e = ('1', '2')
    #ps = [0]
    ps = [0, 0.2, 0.4, 0.5, 0.8, 1]
    x = 3

    for p in ps:
        print(cpdf.Y_coeff_condi(e, p, x_val=x))
        #print(cpdf.eval(e, p_val, x))
        #cpdf.plot(e, p, show=show_plot)
