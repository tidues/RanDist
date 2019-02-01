from scipy.integrate import quad, dblquad
from sympy import lambdify

# numeric gate function
def eta(a, b, x):
    if x >= a and x <= b:
        return 1
    else:
        return 0

# numeric gate function
def etal(a, b, x):
    if x > a and x <= b:
        return 1
    else:
        return 0

# numeric gate function
def etar(a, b, x):
    if x >= a and x < b:
        return 1
    else:
        return 0

# numeric threshold function
def theta(a, b, x):
    if x < a:
        return a
    elif x >b:
        return b
    else:
        return x

# numerical integration with an input expression from sympy
def N_int(expr, range1, range2=None):
    mods = ['numpy', {'theta': theta, 'eta': eta, 'etal': etal, 'etar': etar, 'mmin': min, 'mmax': max}]

    x = range1[0]
    region = [range1[1], range1[2]]

    if range2 is not None:
        y = range2[0]
        var = (y, x)
        yl = lambdify(x, range2[1], modules=mods)
        yu = lambdify(x, range2[2], modules=mods)
        region.append(yl)
        region.append(yu)
        int_func = dblquad
    else:
        var = x
        int_func = quad

    region = tuple(region)

    f = lambdify(var, expr, modules=mods)

    return int_func(f, *region)

# check if input expression is a valid pdf 
# can only verify the integral as 1
# the non-neg need to be guarenteed manually
# only support at most 2-dim input function
def pdf_check(expr, range1, range2=None):
    m, e = N_int(expr, range1, range2)

    if 1 < m - e or 1 > m + e:
        return (False, m, e)
    else:
        return (True, m, e)

    
if __name__ == '__main__':
    from sympy.abc import x,y
    expr = 4 * x * y
    range1 = (x, 0, 1)
    range2 = (y, 0, 1)
    print(pdf_check(expr, range1, range2))



