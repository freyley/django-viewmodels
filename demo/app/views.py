from djviewmodels.views import View

from . import viewmodels
from . import models
from . import forms


class TestView(View):
    template_name = 'test.html'

    viewmodels = {
        'note' : viewmodels.Note,
        }

    def init_request(self, request=None, *args, **kwargs):
        addtl_kwargs = dict(
            foo = 5
        )
        return addtl_kwargs

    def get(self, request=None, *args, **kwargs):
        return dict(
            bar = 6
        )

    def post(self, request=None, *args, **kwargs):
        form = forms.TestForm(data=request.POST)
        if form.is_valid():
            import ipdb; ipdb.set_trace()
