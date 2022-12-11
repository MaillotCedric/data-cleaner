from django.contrib.auth import authenticate

def form(request, input_name):
    """la valeur entrée dans l'input du formulaire

    Args:
        request (Request): requête
        input_name (String): le nom de l'input

    Returns:
        String: ...
    """
    return request.POST[input_name]

def utilisateur(request):
    """l'utilisateur qui tente de s'identifier

    Args:
        request (Request): requête

    Returns:
        Object: ...
    """
    return authenticate(request, username=form(request, "nom_utilisateur"), password=form(request, "mot_de_passe"))

def utilisateur_existe(request):
    """est-ce l'utilisateur est bien enregistré en BDD ?

    Args:
        request (Request): requête

    Returns:
        Boolean: ...
    """
    return utilisateur(request) is not None

def utilisateur_deja_connecte(request):
    """est-ce l'utilisateur est déjà connecté ?

    Args:
        request (Request): requête

    Returns:
        Boolean: ...
    """
    return request.user.is_authenticated
