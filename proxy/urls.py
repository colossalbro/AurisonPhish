from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'^(?P<path>.*)$', Proxy.as_view(), name='proxy')
]