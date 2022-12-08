from django.db import models

class Pays(models.Model):
    Country = models.CharField(primary_key=True, max_length=100)
    class Meta:
        db_table = 'pays'

class Commande(models.Model):
    InvoiceNo = models.CharField(primary_key=True, max_length=100)
    Country = models.ForeignKey(Pays, on_delete=models.CASCADE)
    class Meta:
        db_table = 'commande'

class Produit(models.Model):
    StockCode = models.CharField(primary_key=True, max_length=100)
    class Meta:
        db_table = 'produit'

class Details_commande(models.Model):
    id_details_commande = models.BigAutoField(primary_key=True)
    InvoiceDate = models.DateField()
    InvoiceNo = models.ForeignKey(Commande, on_delete=models.CASCADE)
    StockCode = models.ForeignKey(Produit, on_delete=models.CASCADE)
    class Meta:
        db_table = 'details_commande'
        unique_together = [['InvoiceNo', 'StockCode']]
