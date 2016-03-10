from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='Home'),
    url(r'improve', views.improve, name='Improvements'),
]