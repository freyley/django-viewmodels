from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View as DjangoView
from django.http import HttpResponse
from djviewmodels import utils
from django.utils import simplejson


class Redirect(Exception):
    def __init__(self, *args, **kwargs):
        self.redirect = args[0]
        self.redirect_args = args[1:]
        self.redirect_kwargs = kwargs
        super(Exception, self).__init__(*args, **kwargs)

class APIError(Exception):
    def __init__(self, code, errors, *args, **kwargs):
        self.code = code
        self.errors = errors
        super(APIError, self).__init__(*args, **kwargs)


class View(DjangoView):
    """
    things you can define:
     * http_method_names limits the http_methods that will be allowed
     * template_name sets the template name that will be rendered
     * json sets the view to return json
     * (template_name or json required)
     * define post(self, *args, **kwargs) to receive post requests, get to receive get requests, etc.
     * define viewmodels as a dictionary with variable_name : class to replace
          context variables with the name variable_name with class viewmodels
          wrapped around the original objects
     * define init_request(self, *args, **kwargs) to get access to the request before
          it's passed on to get/post (for setup that's consistent between them).
          return a dictionary and it will be added to kwargs for get, post, etc, and also added to the context for the template
     * override render_template to change the way the context is converted into an http response if template_name is set
     * override render_json to change the way the context is converted into an http response if json is set

    """

    def __init__(self):
        self.template_name = getattr(self, 'template_name', None) or None
        self.json = getattr(self, 'json', None)
        self.viewmodels = getattr(self, 'viewmodels', None)

        if not self.template_name and not self.json:
            raise Exception("template_name or json must be defined") # TODO: better class

    def init_request(self,  request=None, *args, **kwargs): pass
    def get(self, *args, **kwargs): raise NotImplementedError("You should write this.")
    def post(self, *args, **kwargs): raise NotImplementedError("You should write this.")
    def options(self, *args, **kwargs): raise NotImplementedError("You should write this.")
    def head(self, *args, **kwargs): raise NotImplementedError("You should write this.")
    def put(self, *args, **kwargs): raise NotImplementedError("You should write this.")
    def delete(self, *args, **kwargs): raise NotImplementedError("You should write this.")

    def render_template(self, template_name, context, request):
        """ 
        overridable render method
        """
        return render_to_response(self.template_name, context,
                              context_instance=RequestContext(request))


    def render_json(self, context, request):
        """ 
        overridable render method
        """
        resp = HttpResponse(simplejson.dumps(context, 
                                             cls=utils.BetterJSONEncoder),
                            mimetype='application/json')
        resp.status_code = { "POST" : 201, "GET" : 200, "DELETE" : 204, "PUT" : 201 }[request.method]
        return resp


    def dispatch(self, request, *args, **kwargs): # is it call?
        data=None

        # Check allowed methods
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            # TODO: does this properly handle delete and put?
            data = getattr(request, request.method.upper())
        else:
            handler = self.http_method_not_allowed


        # get a response context
        try:
            addtl_kwargs = self.init_request(*args, request=request, **kwargs)
            if addtl_kwargs:
                kwargs.update(addtl_kwargs)
            context = handler(*args, request=request, data=data, **kwargs)
            # bail out early if you return an HttpResponse
            if isinstance(context, HttpResponse):
                return context

            if not context: context = {}
            if addtl_kwargs:
                context.update(addtl_kwargs)
        except Redirect, r:
            return redirect(r.redirect, *r.redirect_args, **r.redirect_kwargs)
        except APIError, apie:
            resp = HttpResponse(simplejson.dumps(apie.errors),
                                mimetype="application/json")
            resp.status_code = apie.code
            return resp

        # translate viewmodels
        if getattr(self, 'viewmodels'):
            for name, cls in self.viewmodels.items():
                if name in context:
                    context[name] = utils._instantiate_viewmodel(cls, context[name], request=request)

        # convert context to a response
        if self.template_name:
            return self.render_template(self.template_name, context, request)

        if self.json:
            return self.render_json(context, request)
