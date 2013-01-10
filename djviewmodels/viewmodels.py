from django.db.models import query

class ViewmodelError(Exception): pass

class Viewmodel(object):
    """ 
        Viewmodel class wraps a model or set of models
        set one of:
         * wrap_each : one viewmodel per model instance
         * wrap_collection : one viewmodel wraps a list or queryset of model instances, and provides aggregate information about all of them

        also receives request and sets it as self.request
    """

    def __init__(self, *args, **kwargs):
        # TODO: this block is for backwards compatibility. Remove it for 1.0.
        self.__fix_for_backwards_compatibility__()

        # TODO: raise an error if self.wrap_collection AND self.wrap_each are both true.
        self.wrap_each = getattr(self, "wrap_each", False)
        self.wrap_collection = getattr(self, "wrap_collection", False)

        if self.wrap_each and self.wrap_collection:
            raise ViewmodelError("%s set to both wrap_each and wrap_collection" % self.__class__)

        # default is wrap_Each
        if not self.wrap_each and not self.wrap_collection:
            self.wrap_each = True

        if self.wrap_each:
            if not args:
                raise ViewmodelError("Must pass at least one instance to a 'wrap_each' viewmodel")
            self.instance = args[0]
        elif self.wrap_collection:
            if not args:
                raise ViewmodelError("Must pass at least one argument to a 'wrap_collection' viewmodel")
            if len(args) == 1 and isinstance(args[0], query.QuerySet):
                args = args[0]
            self.instances = args

        # TODO: handle custom stuff
        self.request = kwargs.get("request")

    def __nonzero__(self):
        if getattr(self, 'wrap_each', False):
            if self.instance:
                return True
            return False
        if getattr(self, 'wrap_collection', False):
            if self.instances:
                return True
            return False
        return True
    def __fix_for_backwards_compatibility__(self):
        if getattr(self, "receive_multiple_instances", False):
            self.wrap_collection = True
        if getattr(self, "receive_single_instance", False):
            self.wrap_each = True

    def __json__(self):
        # TODO: return a json implementation. Perhaps use self.json_fields?
        raise NotImplementedError("You must define __json__ if you want your viewmodel to be converted into json")

    def __getattr__(self, attrName):
        if attrName in ('wrap_each', 'wrap_collection', 
                        'receive_multiple_instances', 'receive_single_instance', 'receive_custom', 
                        'instance',
                        'fields', 'exclude',
                        ):
            pass
        elif self.wrap_each and self.instance:
            try:
                attr = getattr(self.instance, attrName)
                try:
                    fields = self.fields
                except AttributeError:
                    fields = False
                try:
                    exclude = self.exclude
                except AttributeError:
                    exclude = False

                if not fields and not exclude:
                    return attr
                if fields and attrName in fields:
                    return attr
                if exclude and attrName not in exclude:
                    return attr
            except AttributeError: pass
        raise AttributeError(attrName + " not found in " + str(self))
