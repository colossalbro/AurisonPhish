from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eganam/', include('management.urls')),            #manage --> eganam
    path('kramtsop/', include('mails.urls')),      #postmark --> kramtsop
    path('', include('proxy.urls')), 
]
