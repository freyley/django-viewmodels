0.1.0: initial release
0.1.3: fix setup.py
0.1.5: init_request return dict added to template context
0.1.6: bug fix
0.1.7: bug fix in BetterJSONEncoder
0.2.0: now support wrap_each and wrap_collection instead of receive_...
       viewmodel_wrap decorator allows you to wrap the output of a viewmodel function into further viewmodels
0.2.1: memoize added
0.2.2: support truth value testing on viewmodels wrapped around None
0.2.3: typo bug
0.3.0: massive rewrite of __getattr__ (actually works most of the time now)
0.3.1: vm_replace function added to utils to support viewmodel use outside of viewmodel style views
0.3.2: handle put better
0.3.3: load data from request.body in case of json
