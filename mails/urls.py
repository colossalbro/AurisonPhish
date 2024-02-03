from django.urls import path
from .views import *

urlpatterns = [
    path('kramtsop', Webhook.as_view(), name='webhook')     #postmark --> kramtsop
]
