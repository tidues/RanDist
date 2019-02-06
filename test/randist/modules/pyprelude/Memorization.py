

def memorize(ddict, key, func, param_lst=None, param_dict=None, on=True):
    if on is False:
        return runfunc(func, param_lst, param_dict)
    else:
        if key not in ddict:
            ddict[key] = runfunc(func, param_lst, param_dict)

        return ddict[key]


def runfunc(func, param_lst, param_dict):
    if param_lst is None and param_dict is None:
        return func()
    elif param_lst is not None and param_dict is None:
        return func(*param_lst)
    elif param_lst is None and param_dict is not None:
        return func(**param_dict)
    else:
        return func(*param_lst, **param_dict)



