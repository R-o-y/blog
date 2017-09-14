from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^index', views.display_post_index),
    url(r'^$', views.display_post),
    url(r'^upload', views.display_upload_page),    
    url(r'^search', views.search_post),    
    url(r'^handle_upload', views.upload_post),
    url(r'^handle_update', views.update_post),    
]
