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
            return "%d" % obj
        if isinstance(obj, datetime.datetime):
            return obj.ctime()
        return simplejson.JSONEncoder.default(self, obj)


