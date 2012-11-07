class MockModel(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self._save_called = False
    def save(self, *args, **kwargs):
        self._save_called = True


class ModelWrapper(object):
    # TODO: look for fields and excluded

    def __init__(self, model=None, model_kwargs=None, instance=None, **kwargs):
        if model: self.model = model
        if model_kwargs is None: model_kwargs = {}
        if instance:
            self._instance = instance
        else:
            self._instance = self.model(**model_kwargs)
            if getattr(self._instance, 'save') and callable(self._instance.save):
                self._instance.save()

    def __getattr__(self, attrName):
        if attrName in self.__dict__:
            return self.__dict__[attrName]
        if attrName in self._instance.__dict__:
            return self._instance.__dict__[attrName]
        raise AttributeError(attrName + " not found in " + str(self))
