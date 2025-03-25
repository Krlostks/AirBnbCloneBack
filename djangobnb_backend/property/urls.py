from django.urls import path
from . import api
 
urlpatterns = [
     path('', api.properties_detail, name='properties_detail'),
]