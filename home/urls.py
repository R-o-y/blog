from django.conf.urls import url, include
from . import views


urlpatterns = [
    # urls that go to the home page
    url(r'^$', views.display_home_page, name = "home"),
]
