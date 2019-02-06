import randist as rt

# module test switch
switches = {
        'test': 1,
        'cycuni': 0,
        'cycnuni': 0,
        'clinuni': 0,
        'griduni': 0,
        'gridnuni': 0,
        'manhatton': 0
        }

Stats = rt.Stats

if switches['test'] == 1:
    gname = 'g0'
    phiname = 'uniform'
    cdf = rt.load_formulas(gname, phiname, Stats.CDF)
    print(cdf.eval(5))
    #print(cdf.formula())
    cdf.plot()
    pdf = rt.load_formulas(gname, phiname, Stats.PDF)
    print(pdf.eval(5))
    #print(pdf.formula())
    pdf.plot()
    loc1 = (('1', '2'), 0.2)
    loc2 = (('1', '3'), 0.5)
    loc3 = (('3', '4'), 0)
    locs = [loc1, loc2, loc3]
    ccdf = rt.load_formulas(gname, phiname, Stats.CCDF)
    for loc in locs:
        print(ccdf.eval(*loc, 5))
        #print(ccdf.formula(*loc))
        ccdf.plot(*loc)
    cpdf = rt.load_formulas(gname, phiname, Stats.CPDF)
    for loc in locs:
        print(cpdf.eval(*loc, 5))
        #print(cpdf.formula(*loc))
        cpdf.plot(*loc)

if switches['cycuni'] == 1:
    gname = 'gcyc'
    phiname = 'uniform'
    cdf = rt.load_formulas(gname, phiname, Stats.CDF)
    cdf.plot()
    pdf = rt.load_formulas(gname, phiname, Stats.PDF)
    pdf.plot()

if switches['cycnuni'] == 1:
    gname = 'gcyc'
    phiname = 'pqbeta'
    pdf = rt.load_formulas(gname, phiname, Stats.PDF)
    pdf.plot()

if switches['clinuni'] == 1:
    gname = 'gcli'
    phiname = 'qbeta'
    pdf = rt.load_formulas(gname, phiname, Stats.PDF)
    pdf.plot()
    cpdf = rt.load_formulas(gname, phiname, Stats.CPDF)
    loc1 = (('1', '2'), 0.2)
    loc2 = (('1', '3'), 0.5)
    loc3 = (('3', '4'), 0)
    cpdfp = [loc1, loc2, loc3]
    for loc in cpdfp:
        cpdf.plot(*loc)

if switches['griduni'] == 1:
    gname = 'planar_side_10'
    phiname = 'uniform'
    pdf = rt.load_formulas(gname, phiname, Stats.PDF)
    pdf.plot()
    cpdf = rt.load_formulas(gname, phiname, Stats.CPDF)
    loc1 = (('1', '2'), 0)
    loc2 = (('5', '6'), 0.5)
    loc3 = (('45', '46'), 0.5)
    cpdfp = [loc1, loc2, loc3]
    for loc in cpdfp:
        cpdf.plot(*loc)

if switches['gridnuni'] == 1:
    gname = 'planar_side_10'
    phiname = 'qbeta'
    pdf = rt.load_formulas(gname, phiname, Stats.PDF)
    pdf.plot()
    cpdf = rt.load_formulas(gname, phiname, Stats.CPDF)
    loc1 = (('1', '2'), 0)
    loc2 = (('5', '6'), 0.5)
    loc3 = (('45', '46'), 0.5)
    loc4 = (('45', '46'), 0.6)
    cpdfp = [loc1, loc2, loc3]
    for loc in cpdfp:
        cpdf.plot(*loc)

if switches['manhatton'] == 1:
    pass
