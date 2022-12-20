from rest_framework import serializers
from django.contrib.auth.models import User
from etl.models import *
from django.contrib.auth.hashers import make_password

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        
        return super(UsersSerializer, self).create(validated_data)

class SalesByProductsSerializer(serializers.ModelSerializer):
    stock_code = serializers.CharField()
    nb_ventes = serializers.IntegerField()

    class Meta:
        model = Details_commande
        fields = ["stock_code", "nb_ventes"]

class SalesByCountriesSerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    nb_ventes = serializers.IntegerField()

    class Meta:
        model = Details_commande
        fields = ["country", "nb_ventes"]

class SalesOfSerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    stock_code = serializers.CharField()
    nb_ventes = serializers.IntegerField()

    class Meta:
        model = Details_commande
        fields = ["country", "stock_code", "nb_ventes"]

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ["country"]

class YearsSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()

    class Meta:
        model = Details_commande
        fields = ["year"]
