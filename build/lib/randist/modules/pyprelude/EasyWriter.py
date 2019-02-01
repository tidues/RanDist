import os
import errno


# function write file
# help create folders recursively if doesn't exist
# support append as well as write
def wFile(ffname, output, writetype='a'):
    dirname = os.path.dirname(ffname)
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if not os.path.isfile(ffname):
        wtype = 'w'
    else:
        wtype = writetype

    wf = open(ffname, wtype)
    wf.write(output)
    wf.close()
