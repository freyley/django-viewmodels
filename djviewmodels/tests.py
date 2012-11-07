from django.test import TestCase
from djviewmodels.test_views import *

class MockRequest(object):
    pass

class ViewmodelTests(TestCase):
    def test_viewmodel_basics(self):
        item = Item(1)
        viewmodel = ItemViewmodel(item)
        retail_vm = RetailItem(item)
        wh_vm = WholesalerItem(item)
        self.assertEqual(40, viewmodel.cost)
        self.assertEqual(40, retail_vm.cost)
        self.assertEqual(40, wh_vm.cost)
        self.assertRaises(AttributeError, lambda: viewmodel.price)
        self.assertEqual(50, wh_vm.price)
        self.assertEqual(540, retail_vm.price)
        self.assertEqual(wh_vm.instance, retail_vm.instance)

    def test_viewmodel_fields_passthrough(self):
        item = Item(4)
        wh_item = WholesalerItem(item)
        self.assertEqual(160, wh_item.cost)
        self.assertEqual(10, wh_item.wh_markup)
        self.assertRaises(AttributeError, lambda: wh_item.retail_markup)
        self.assertEqual(170, wh_item.price)

    def test_viewmodel_exclude_excludes(self): 
        item = Item(2)
        retail_item = RetailItem(item)
        self.assertEqual(500, retail_item.retail_markup)
        self.assertRaises(AttributeError, lambda: retail_item.wh_markup)
        self.assertEqual(580, retail_item.price)
        
class ViewTests(TestCase):
    def test_viewmodel_conversion(self):
        view = ItemView.as_view()
        request = MockRequest()
        request.method = 'GET'
        request.GET = {}
        request.user = MockRequest()
        request.user.type = 'wholesaler'
        template_name, context = view(request, item_id=2.5)
        self.assertEqual('item.html', template_name)
        self.assertEqual(110, context['item'].price)
        self.assertEqual(WholesalerItem, type(context['item']))
        request.user.type = 'retailer'
        template_name, context = view(request, item_id=2.5)
        self.assertEqual(RetailItem, type(context['item']))
        self.assertEqual(600, context['item'].price)
                         
        
    def test_init_request_return_passthrough(self): pass
    def test_Redirect_exception_handler(self): 
        # TODO
        pass

class JSONViewTests(TestCase):
    pass
