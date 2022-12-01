from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UsersSerializer

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
