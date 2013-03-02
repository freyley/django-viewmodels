django-viewmodels
=================

Automatic viewmodel conversion for django class-based views

* import View from djviewmodels.views and use it as a base class
** define viewmodels as a dictionary (key: variable name in context, value: class to replace with)
          for automatic conversion of variables in the returned context to viewmodels
** define get, post, put, delete as methods to handle those requests, return a context dictionary
** define init_request as a generic method to handle the beginning of all requests
*** init_request can return a dictionary, whose values will be passed to get/post/whoever
*** init_request returned dictionary will be added to template context
** define template_name or json
*** template_name will cause context dictionaries to be rendered to that template
*** json will cause context dictionaries to be rendered to json

* Automatic viewmodel extension of models:
** define wrap_each to have individual viewmodels wrapped around individual models
*** __getattr__ will look inside the instance for fields
*** define fields to specify which fields to allow automatic retrieval of
*** define exclude to exclude fields
** define wrap_collection to have the viewmodel wrap around the whole list

* deprecated receive_single_instance and receive_multiple_instances still functional until v1.0

* viewmodel replacement function and decorator can be used in viewmodels or views without the class based view of django viewmodels:
** djviewmodels.utils.vm_replace(cls, obj_or_list, request=None) accepts a viewmodel class, an object or list, and an optional request, and returns viewmodels
** djviewmodels.decorators.viewmodel_wrap(cls) wraps a function that returns some value and turns that value into cls-based viewmodels. Looks for self.request on methods.

See the tests for more information and usage
