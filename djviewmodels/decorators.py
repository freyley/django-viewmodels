from djviewmodels.utils import _instantiate_viewmodel

def viewmodel_wrap(cls):
    if type(cls) == str:
        # TODO: import the string as a class
        pass
    def fnc(fn):
        def wrap(*args, **kwargs):
            retval = fn(*args, **kwargs)
            # try to find self, and from there, request
            request = None
            if args:
                self = args[0]
                request = getattr(self, 'request', None)
            
            return _instantiate_viewmodel(cls, retval, request=request)
        return wrap
    return fnc

