from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
from .forms import UploadFileForm
from .clean import nettoyer

def render_etl(request):
    form = UploadFileForm()

    return render(request, "etl.html", {"form": form})

@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            # encodage du fichier
            file = TextIOWrapper(request.FILES['fichier'], encoding="iso-8859-1", newline="")

            # processus de nettoyage ( version 1 )
            nettoyer(file)

            return render(request, "etl.html", {"form": form})
        else:
            return render_etl(request)
    else:
        return render_etl(request)
