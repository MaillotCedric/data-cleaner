from django.contrib import admin
from .models import Pays, Commande, Produit, Details_commande

admin.site.register(Pays)
admin.site.register(Commande)
admin.site.register(Produit)
admin.site.register(Details_commande)
