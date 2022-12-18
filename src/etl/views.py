from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
from .forms import UploadFileForm
from .clean import nettoyage
from .outils_bdd import get_engine
from .update import update_bdd
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
            
            data_frame = resultat["data_frame"]
            # modification du nom des colonnes (suppression des maj. dans le nom des colonnes)
            data_frame.columns = ["invoice_no", "stock_code", "invoice_date", "country"]
            # création d'une table temporaire qui va représenter le dataframe nettoyé
            bdd_engine = get_engine()
            data_frame.to_sql('df_nettoye', con=bdd_engine, index=False, if_exists='replace')

            return render(request, "etl.html", {"form": form, "feedback": resultat["feedback"], "import_bdd": True})
        else:
            return render_etl(request)
    else:
        return render_etl(request)

def add_bdd(request):
    update_bdd()

    return redirect("etl")
