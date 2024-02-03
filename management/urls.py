from django.urls import path
from .views import *

urlpatterns = [
    path('camp/<int:id>/delete', DeleteCampaign.as_view(), name='delete_campaign'),
    path('camp/<int:id>/info', CampaignStats.as_view(), name='get_campaign_stats'),
    path('camp/<int:id>/start', startCampaign.as_view(), name='start_campaign'),
    path('camp/<int:id>/stop', stopCampaign.as_view(), name='stop_campaign'),
    path('camp/<int:id>', GetCampaign.as_view(), name='get_campaign'),
    path('camp/all', GetCampaign.as_view(), name='all_campaigns'),
    path('upload', NewCampaign.as_view(), name='upload'),
    path('camp/new', NewCampaign.as_view(), name='new'),
    path('login', Login.as_view(), name='login_post'),
    path('logout', Logout.as_view(), name='logout'),
    path('camp', Home.as_view(), name='home'),
    path('', Login.as_view(), name='x'),
]