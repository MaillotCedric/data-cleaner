from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UsersSerializer, SalesByProductsSerializer

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
        SELECT (1) AS id, stock_code_id, stock_code, count(*) AS nb_ventes
            FROM details_commande AS dc
            INNER JOIN produit AS pr
                ON dc.stock_code_id = pr.id
            GROUP BY (1), stock_code_id, stock_code
            ORDER BY nb_ventes DESC
            {};
    """.format(limite)

    sales_by_products = User.objects.raw(requeteSQL)
    serializer = SalesByProductsSerializer(sales_by_products, many=True)

    return Response(serializer.data)
