from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .auth_tools import *

def index(request):
    if request.method == "POST":
        if utilisateur_existe(request):
            login(request, utilisateur(request)) # on se connecte
            
            return redirect("etl")
        return render(request, "login.html", {})
    else:
        if utilisateur_deja_connecte(request):
            # etl.html est définie comme page d'accueil par défaut pour un utilisateur connecté
            return redirect("/etl")
        else:
            return render(request, "login.html", {})

def logout_utilisateur(request):
    logout(request) # on se déconnecte

    return redirect("login") # on est redirigé vers la page de login
