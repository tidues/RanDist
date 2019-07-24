from .formulas import Formulas
from .enums import Stats

# info_dict keys and values
# moment: ks; cdf: nothing; pdf: nothing;
# cmoment: (ks, locs); ccdf: locs; cpdf: locs
# cdfe: xs; pdfe: xs; ccdfe: loc+x; cpdfe: loc+x
def data_collector(gname, phi, mmtp=False, cdfp=False, cdfe=False, pdfp=False, pdfe=False, cmmtp=False, ccdfp=False, ccdfe=False, cpdfp=False, cpdfe=False, d_jit=False, memorize=True, timing=True):
    fls = Formulas(gname, phi, d_jit=d_jit, memorize=memorize)

    # moments
    if mmtp is not False and mmtp['collect']:
        moment = fls.get_formula(Stats.MOMENT, symbolic=mmtp['symbolic'])
        for k in mmtp['valst']:
            moment.eval(k, timing=timing)

    # cdf
    if cdfp is not False and cdfp['collect']:
        cdf = fls.get_formula(Stats.CDF, symbolic=cdfp['symbolic'])
        cdf.plot()
        if cdfp['symbolic']:
            cdf.save_formulas()

    # cdfe
    if cdfe is not False and cdfe['collect']:
        cdf = fls.get_formula(Stats.CDF, symbolic=cdfp['symbolic'])
        for x in cdfe['valst']:
            cdf.eval(x, timing=timing)
        if cdfe['symbolic']:
            cdf.save_formulas()

    # pdf
    if pdfp is not False and pdfp['collect']:
        pdf = fls.get_formula(Stats.PDF, symbolic=pdfp['symbolic'])
        pdf.plot()
        if pdfp['symbolic']:
            pdf.save_formulas()

    # pdf
    if pdfe is not False and pdfe['collect']:
        pdf = fls.get_formula(Stats.PDF, symbolic=pdfp['symbolic'])
        for x in pdfe['valst']:
            pdf.eval(x, timing=timing)
        if pdfe['symbolic']:
            pdf.save_formulas()

    # cmoments
    if cmmtp is not False and cmmtp['collect']:
        cmoment = fls.get_formula(Stats.CMOMENT, symbolic=cmmtp['symbolic'])
        for k in cmmtp['valst'][0]:
            for loc in cmmtp['valst'][1]:
                cmoment.eval(k, *loc, timing=True)

    # ccdf
    if ccdfp is not False and ccdfp['collect']:
        ccdf = fls.get_formula(Stats.CCDF, symbolic=ccdfp['symbolic'])
        for loc in ccdfp['valst']:
            ccdf.plot(*loc)
        if ccdfp['symbolic']:
            ccdf.save_formulas()

    # ccdfe
    if ccdfe is not False and ccdfe['collect']:
        ccdf = fls.get_formula(Stats.CCDF, symbolic=ccdfp['symbolic'])
        for locx in ccdfe['valst']:
            ccdf.eval(*locx, timing=timing)
        if ccdfe['symbolic']:
            ccdf.save_formulas()

    # cpdf
    if cpdfp is not False and cpdfp['collect']:
        cpdf = fls.get_formula(Stats.CPDF, symbolic=cpdfp['symbolic'])
        for loc in cpdfp['valst']:
            cpdf.plot(*loc)
        if cpdfp['symbolic']:
            cpdf.save_formulas()

    # cpdfe
    if cpdfe is not False and cpdfe['collect']:
        cpdf = fls.get_formula(Stats.CPDF, symbolic=cpdfp['symbolic'])
        for locx in cpdfe['valst']:
            cpdf.eval(*locx, timing=timing)
        if cpdfe['symbolic']:
            cpdf.save_formulas()
