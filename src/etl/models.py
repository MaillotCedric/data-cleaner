from django.db import models

class Pays(models.Model):
    country = models.CharField(primary_key=True, max_length=100)
    class Meta:
        db_table = 'pays'
        # constraints = [
        #     models.UniqueConstraint(fields=["country"], name="country unique")
        # ]

class Commande(models.Model):
    invoice_no = models.CharField(primary_key=True, max_length=100)
    country = models.ForeignKey(Pays, on_delete=models.CASCADE)
    class Meta:
        db_table = 'commande'
        # constraints = [
        #     models.UniqueConstraint(fields=["invoice_no"], name="invoice_no unique")
        # ]

class Produit(models.Model):
    stock_code = models.CharField(primary_key=True, max_length=100)
    class Meta:
        db_table = 'produit'
        # constraints = [
        #     models.UniqueConstraint(fields=["stock_code"], name="stock_code unique")
        # ]

class Details_commande(models.Model):
    invoice_date = models.DateField()
    invoice_no = models.ForeignKey(Commande, on_delete=models.CASCADE)
    stock_code = models.ForeignKey(Produit, on_delete=models.CASCADE)
    class Meta:
        db_table = 'details_commande'
        unique_together = [['invoice_no', 'stock_code']]
