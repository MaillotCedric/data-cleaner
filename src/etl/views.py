from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
from .forms import UploadFileForm
from .clean import nettoyage
from django.template.defaulttags import register

@register.filter("get_key")

def get_key(dict_data, key):
    """Usage example {{ your_dict|get_key:your_key }}
    """
    if key:
        return dict_data.get(key)

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
            resultat = nettoyage(file)

            return render(request, "etl.html", {"form": form, "feedback": resultat["feedback"]})
        else:
            return render_etl(request)
    else:
        return render_etl(request)
