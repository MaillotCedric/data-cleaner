from django.db import models

class Pays(models.Model):
    country = models.CharField(primary_key=True, max_length=100)
    class Meta:
        db_table = 'pays'

class Commande(models.Model):
    invoice_no = models.CharField(primary_key=True, max_length=100)
    country = models.ForeignKey(Pays, on_delete=models.CASCADE)
    class Meta:
        db_table = 'commande'

class Produit(models.Model):
    stock_code = models.CharField(primary_key=True, max_length=100)
    class Meta:
        db_table = 'produit'

class Details_commande(models.Model):
    id_details_commande = models.BigAutoField(primary_key=True)
    invoice_date = models.DateField()
    invoice_no = models.ForeignKey(Commande, on_delete=models.CASCADE)
    stock_code = models.ForeignKey(Produit, on_delete=models.CASCADE)
    class Meta:
        db_table = 'details_commande'
        unique_together = [['invoice_no', 'stock_code']]
