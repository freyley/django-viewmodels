from django.utils import simplejson
from decimal import Decimal
import datetime

class BetterJSONEncoder(simplejson.JSONEncoder):
    """JSON encoder which understands decimals, dates, and __json__"""

    def default(self, obj):
        '''Convert object to JSON encodable type.'''
        if hasattr(obj, '__json__'):
            return obj.__json__()
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return simplejson.JSONEncoder.default(self, obj)


def _instantiate_viewmodel(cls, obj, request=None):
    """
    This class instantiates viewmodels around objects. It is the class that
    pays attention to whether a viewmodel should wrap an entire collection of objects
    or whether it should iterate the collection and wrap each item.

    self.wrap_collection: wrap collection
    self.wrap_each: iterate, and wrap each

    """
    if getattr(cls, "wrap_collection", False):
        return cls(obj, request=request)
    else:
        if getattr(obj,'__iter__', False):
            return [ cls(o, request=request) for o in obj ]
        else:
            return cls(obj, request=request)

    # TODO: some kind of self.custom setting...??? a constructor?
