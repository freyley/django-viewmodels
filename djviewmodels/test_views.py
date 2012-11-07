from djviewmodels.views import View, Redirect
from djviewmodels.viewmodels import Viewmodel

class Item(object):

    def __init__(self, id):
        self.cost = 40 * id
        self.wh_markup = 10
        self.retail_markup = 500

class ItemViewmodel(Viewmodel):
    model = Item
    receive_single_instance = True
    
class WholesalerItem(Viewmodel):
    model = Item
    receive_single_instance = True
    fields = ['cost', 'wh_markup']
    
    @property
    def price(self):
        return self.cost + self.wh_markup

class RetailItem(Viewmodel):
    model = Item
    receive_single_instance = True
    exclude = ['wh_markup']

    @property
    def price(self):
        return self.cost + self.retail_markup

class ItemView(View):
    viewmodels = { }
    template_name = 'item.html'

    def render_template(self, template_name, context, request):
        return (template_name, context)

    def init_request(self, request=None, item_id=None, *args, **kwargs):
        if request.user.type == 'wholesaler':
            self.viewmodels['item'] = WholesalerItem
        else:
            self.viewmodels['item'] = RetailItem
        if not item_id:
            raise Redirect("item_list")
        item = Item(item_id)
        return dict(item=item)

    def get(self, request=None, item=None, *args, **kwargs):
        return dict(item=item)

    def post(self, request=None, item=None, *args, **kwargs):
        request.item = item
        raise Redirect("cart")



