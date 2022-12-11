from django.urls import path
from . import views

urlpatterns = [
    path("users", views.get_utilisateurs, name="get_utilisateurs"),
    path("add", views.add_utilisateur, name="add_utilisateur"),
    path("sales_by_products", views.get_sales_by_products, name="get_sales_by_products"),
    path("sales_by_countries", views.get_sales_by_countries, name="get_sales_by_countries"),
    path("sales_of", views.get_sales_of, name="get_sales_of")
]
