from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'map', views.map, name='Neighborhood Map'),
]

urlpatterns += staticfiles_urlpatterns()