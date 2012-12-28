from djviewmodels.views import View, Redirect
from djviewmodels.viewmodels import Viewmodel

class Item(object):

    def __init__(self, id):
        self.cost = 40 * id
        self.wh_markup = 10
        self.retail_markup = 500

class ItemViewmodel(Viewmodel):
    model = Item
    wrap_each = True

class WholesalerItem(Viewmodel):
    model = Item
    wrap_each = True
    fields = ['cost', 'wh_markup']
    
    @property
    def price(self):
        return self.cost + self.wh_markup

class RetailItem(Viewmodel):
    model = Item
    wrap_each = True
    exclude = ['wh_markup']

    @property
    def price(self):
        return self.cost + self.retail_markup

class ItemAggregate(Viewmodel):
    wrap_collection = True
    model = Item

    def total_price(self):
        total = 0.0
        for item in self.instances:
            total += item.cost
        return total

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


class CartView(View):
    template_name = 'cart.html'
    viewmodels = dict(
            items = ItemViewmodel,
            cart_total = ItemAggregate,
    )

    def get(self, request=None, *args, **kwargs):
        items = request.session.get("cart")
        return dict(
                items=items,
                cart_total=items,)

