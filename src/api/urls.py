from django.urls import path
from . import views

urlpatterns = [
    path("users", views.get_utilisateurs, name="get_utilisateurs"),
    path("add", views.add_utilisateur, name="add_utilisateur")
]
