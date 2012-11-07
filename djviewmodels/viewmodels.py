from django.db.models import query

class ViewmodelError(Exception): pass

class Viewmodel(object):
    receive_single_instance = True
    receive_multiple_instances = False
    receive_custom = False

    def __init__(self, *args, **kwargs):
        if self.receive_single_instance:
            if not args:
                raise ViewmodelError("Must pass an instance to a single instance viewmodel")
            self.instance = args[0]
        elif self.receive_multiple_instances:
            if not args:
                raise ViewmodelError("Must pass instances to a multiple instance viewmodel")
            if len(args) == 1 and isinstance(args[0], query.QuerySet):
                args = args[0]
            self.instances = args
        elif self.receive_custom:
            self.custom_args = args
            self.custom_kwargs = kwargs
        self.request = kwargs.get("request")

    def __json__(self):
        # TODO: return a json implementation. Perhaps use self.json_fields?
        raise NotImplementedError("You must define __json__ if you want your viewmodel to be converted into json")

    def __getattr__(self, attrName):

        if attrName in self.__dict__:
            return self.__getitem__(attrName)

        if self.receive_single_instance:
            instance = self.__dict__['instance']
            
            try:
                attr = getattr(instance, attrName)
                try:
                    fields = self.fields
                except AttributeError:
                    try:
                        fields = self.__dict__['fields']
                    except KeyError:
                        fields = None

                try:
                    exclude = self.exclude
                except AttributeError:
                    try:
                        exclude = self.__dict__['exclude']
                    except KeyError:
                        exclude = None

                if not fields and not exclude:
                    return attr
                if fields and attrName in fields:
                    return attr
                if exclude and attrName not in exclude:
                    return attr
            except AttributeError: pass
        raise AttributeError(attrName + " not found in " + str(self))    

