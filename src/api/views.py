from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import *

@api_view(["GET"])
def get_utilisateurs(request):
    utilisateurs = User.objects.all()
    serializer = UsersSerializer(utilisateurs, many=True)

    return Response(serializer.data)

@api_view(["POST"])
def add_utilisateur(request):
    # new_user = {
    #     "username": "admin2",
    #     "email": "admin2@example.com",
    #     "password": "azerty",
    #     "is_staff": true,
    #     "is_superuser": true
    # }
    # serializer = UsersSerializer(data=new_user)
    
    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)

@api_view(["GET"])
def get_sales_by_products(request):
    top = request.query_params.get("top", None)
    limite = "LIMIT {}".format(top) if top else ""

    requeteSQL = """
        SELECT (1) AS id, stock_code, COUNT(*) AS nb_ventes
            FROM details_commande AS dc
                INNER JOIN produit AS pr
                    ON dc.stock_code_id = pr.id
            GROUP BY (1), stock_code
            ORDER BY nb_ventes DESC
            {};
    """.format(limite)

    sales_by_products = User.objects.raw(requeteSQL)
    serializer = SalesByProductsSerializer(sales_by_products, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def get_sales_by_countries(request):
    top = request.query_params.get("top", None)
    limite = "LIMIT {}".format(top) if top else ""

    requeteSQL = """
        SELECT (1) AS id, country, COUNT(*) AS nb_ventes
            FROM details_commande AS dc
                INNER JOIN commande AS co
                    ON dc.invoice_no_id = co.id
                INNER JOIN pays AS pa
                    ON co.country_id = pa.id
            GROUP BY (1), country
            ORDER BY nb_ventes DESC
            {};
    """.format(limite)

    sales_by_countries = User.objects.raw(requeteSQL)
    serializer = SalesByCountriesSerializer(sales_by_countries, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def get_sales_of(request):
    pays = request.query_params.get("pays", None)
    top = request.query_params.get("top", None)
    where = "WHERE country = '{}'".format(pays) if pays else ""
    print(where)
    limite = "LIMIT {}".format(top) if top else ""

    requeteSQL = """
        SELECT (1) AS id, country, stock_code, COUNT(*) as nb_ventes
            FROM details_commande AS dc
                INNER JOIN produit AS pr
                    ON dc.stock_code_id = pr.id
                INNER JOIN commande AS co
                    ON dc.invoice_no_id = co.id
                INNER JOIN pays AS pa
                    ON co.country_id = pa.id
            {}
            GROUP BY (1), country, stock_code
            ORDER BY country ASC
            {};
    """.format(where, limite)

    sales_of = User.objects.raw(requeteSQL)
    serializer = SalesOfSerializer(sales_of, many=True)

    return Response(serializer.data)
