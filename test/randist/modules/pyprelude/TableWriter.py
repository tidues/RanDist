from . import FPToolBox as fp
from . import EasyWriter as ew

""" output a table from nested list input"""
def tableStrFormat(lst, cSep='\t', rSep='\n'):

    cConcat = fp.concat(cSep)
    rConcat = fp.concat(rSep)

    def formRow(lst1):
        return fp.foldr(cConcat, fp.lmap(str, lst1), '')[:-1]

    return fp.foldr(rConcat, fp.lmap(formRow, lst), '')[:-1]


""" form and write the table """
# formatType: b: bueaty, n: normal
def tableWrite(lst, wfname, cSep='\t', rSep='\n', wtype='w', formatType='b', numCols=[], padNum=2):
    if formatType == 'b':
        output = tableBeautyFormat(lst, numCols, padNum)
    else:
        output = tableStrFormat(lst, cSep, rSep)
    ew.wFile(wfname, output, wtype)


""" formart list of lists with better presentation """
def tableBeautyFormat(lst0, numCols=[], padNum=2):

    # change all value to string
    lst = []
    for row in lst0:
        lst.append(fp.lmap(str, row))

    # get the nth column
    maxLen = []
    for i in range(len(lst[0])):
        tmpCol = nthCol(lst, i)
        lenLst = fp.lmap(len, tmpCol)
        maxLen.append(max(lenLst) + padNum)
    
    # direction list
    dirLst = ['left'] * len(lst[0])
    for i in numCols:
        dirLst[i] = 'right'
    
    # for each row do padding
    def resize(vlst, lenLst, dirLst):
        res = fp.zipWith3(padding, vlst, maxLen, dirLst)
        return res

    bueatyLst = fp.lmap(lambda x: resize(x, lenLst, dirLst), lst)
    return tableStrFormat(bueatyLst, cSep='')


""" padding function"""
def padding(s, padLen, dirc, padChar=' '):
    if padLen <= len(s):
        return s
    l = padLen - len(s)
    if dirc == 'left':
        s1 = padChar + s + (padChar * l)
    else:
        s1 = (padChar * l) + s + padChar
    return s1


""" get the nth column of a nested list """
def nthCol(lst, n, f=lambda x: x):
    return fp.lmap(lambda x: f(x[n]), lst)
    


# mylst = [["testa", 2, 3], [2, "testttttb", 4], [4, 5, "testc01"]]
# print(tableBeautyFormat(mylst, [1]))
# print(padding('testa', 7, 'left', padChar=' '))
# print(tableStrFormat(mylst))
