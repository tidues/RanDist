# (a->b->b)->[a]->b
def foldr(f, slst, binit):
    while slst != []:
        last = slst[-1]
        slst = slst[:-1]
        binit = f(last, binit)
    return binit


# (a->b)->[a]->[b]
def lmap(f, aLst):
    return [f(a) for a in aLst]


# composition
def comp(f, g):
    return lambda x: f(g(x))


# string concat
def concat(sep):
    def myconcat(v1, v2):
        return str(v1) + sep + str(v2)
    return myconcat


# zip two list with function
# (a -> b -> c) -> [a] -> [b] -> [c]
def zipWith(f, alst, blst):
    res = []
    for i in range(min(len(alst), len(blst))):
        res.append(f(alst[i], blst[i]))
    return res


# zip three lists with function
# (a -> b -> c -> d) -> [a] -> [b] -> [c] -> [d]
def zipWith3(f, alst, blst, clst):
    res = []
    for i in range(min(len(alst), len(blst), len(clst))):
        res.append(f(alst[i], blst[i], clst[i]))
    return res


# filter
# (a -> bool) -> [a] -> [a]
def filter(f, aLst):
    return [a for a in aLst if f(a)]


# count number of items in list satisfy predicate
def countIf(p, lst):
    return len(filter(p, lst))

