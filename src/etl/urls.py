from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='etl'),
    path('add_bdd', views.add_bdd, name='add_bdd')
]
