from . import FPToolBox as fp
from . import StringTools as st

# function that read data into double list
def dataFormat(ffname, start_row=0, seps='\t '):
    rf = open(ffname, 'r')
    lst = []
    for line in rf:
        line = line.strip()
        lst.append(fp.lmap(strip, st.splitOneOf(line, seps)))
    rf.close()
    return lst


# function for strip
def strip(strs):
    return strs.strip()
