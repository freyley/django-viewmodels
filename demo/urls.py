from django.conf.urls.defaults import patterns, url
from app import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.TestView.as_view(), name='test_view'),
)
