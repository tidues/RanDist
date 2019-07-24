from . import FPToolBox as fp

# split one of the char in
def splitOneOf(s, seps, delEmpty=True):
    sep0 = seps[0]
    sepTail = seps[1:]
    sLst = s.split(sep0)
    for c in sepTail:
        tmpLst = fp.lmap(lambda x: x.split(c), sLst)
        sLst = fp.foldr(lambda x, y: x + y, tmpLst, [])

    if delEmpty is True:
        sLst = fp.filter(lambda x: x != '', sLst)

    return sLst

