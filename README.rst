django-viewmodels
=================

Automatic viewmodel conversion for django class-based views

* import View from djviewmodels.views and use it as a base class
** define viewmodels as a dictionary (key: variable name in context, value: class to replace with)
          for automatic conversion of variables in the returned context to viewmodels
** define get, post, put, delete as methods to handle those requests, return a context dictionary
** define init_request as a generic method to handle the beginning of all requests
*** init_request can return a dictionary, whose values will be passed to get/post/whoever
** define template_name or json
*** template_name will cause context dictionaries to be rendered to that template
*** json will cause context dictionaries to be rendered to json

* Automatic viewmodel extension of models:
** define receive_single_instance to have individual viewmodels wrapped around individual models
*** __getattr__ will look inside the instance for fields
*** define fields to specify which fields to allow automatic retrieval of
*** define exclude to exclude fields
** define receive_multiple_instances to have the viewmodel wrap around the whole list
** define receive_custom to receive the list or dictionary as args/kwargs

See the tests for more information and usage
