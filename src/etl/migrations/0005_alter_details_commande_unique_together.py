# Generated by Django 4.1.3 on 2022-12-08 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0004_details_commande'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='details_commande',
            unique_together={('InvoiceNo', 'StockCode')},
        ),
    ]
