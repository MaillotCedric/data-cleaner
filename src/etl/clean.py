from .outils import *

def get_pourcentage(nombre_lignes, feedback):
    pourcentage_exact = (100 * nombre_lignes) / feedback["nombre enregistrements"]

    return formate(pourcentage_exact) if pourcentage_exact >= 0.01 else "0 %" if pourcentage_exact == 0 else "< 0.01 %"

def get_nb_lignes_apres_supp(df, nombre_lignes):
    return df.shape[0] - nombre_lignes

def get_feedback_doublons(df, subset, feedback):
    pd_serie = mask_doublons(df, subset).value_counts()
    nombre_lignes = pd_serie["doublon"]

    feedback["etapes"].append({
        "nom": "suppression des doublons",
        "critère": "InvoiceNo et StockCode identiques",
        "nombre lignes supprimées": nombre_lignes,
        "nombre lignes après suppression": get_nb_lignes_apres_supp(df, nombre_lignes),
        "pourcentage global": get_pourcentage(nombre_lignes, feedback)
    })

def get_feedback_avoirs(df, feedback):
    pd_serie = mask_avoirs(df).value_counts()
    nombre_lignes = pd_serie["avoir"]

    feedback["etapes"].append({
        "nom": "suppression des avoirs",
        "critère": "Quantity <= 0",
        "nombre lignes supprimées": nombre_lignes,
        "nombre lignes après suppression": get_nb_lignes_apres_supp(df, nombre_lignes),
        "pourcentage global": get_pourcentage(nombre_lignes, feedback)
    })

def get_details_feedback_stock_code(df, stock_codes_invalides, feedback):
    details_stock_code = {
        "nombre lignes": 0,
        "feedback": []
    }

    for stock_code in stock_codes_invalides:
        nombre_lignes = nombre_produits(df, stock_code)

        details_stock_code["feedback"].append({
            "stock_code": stock_code,
            "nombre lignes supprimées": nombre_lignes,
            "pourcentage global": get_pourcentage(nombre_lignes, feedback)
        })

        details_stock_code["nombre lignes"] += nombre_lignes

    return details_stock_code

def get_feedback_stock_codes(df, stock_codes_invalides, feedback):
    details = get_details_feedback_stock_code(df, stock_codes_invalides, feedback)
    nombre_lignes = details["nombre lignes"]

    feedback["etapes"].append({
        "nom": "suppression des ventes avec des stock codes invalides",
        "critère": "StockCode invalides : ['S', 'POST', 'M', 'DOT', 'D', 'BANK CHARGES', 'AMAZONFEE']",
        "details": details["feedback"],
        "nombre lignes supprimées": nombre_lignes,
        "nombre lignes après suppression": get_nb_lignes_apres_supp(df, nombre_lignes),
        "pourcentage global": get_pourcentage(nombre_lignes, feedback)
    })

def nettoyage(fichier):
    # --------------- variables -----------------------
    feedback = {
        "nombre enregistrements": 0,
        "etapes": []
    }
    subset = ["InvoiceNo", "StockCode"]
    stock_codes_invalides = ["S", "POST", "M", "DOT", "D", "BANK CHARGES", "AMAZONFEE"]
    # -------------------------------------------------

    # get data frame
    df = data_frame(fichier)

    # set nombre enregistrements
    feedback["nombre enregistrements"] = df.shape[0]
    
    # ------------ gestion des doublons ---------------
    # feedback
    get_feedback_doublons(df, subset, feedback)
    # suppression
    df.drop_duplicates(subset=subset, inplace=True)
    # -------------------------------------------------

    # ------------ gestion des avoirs ---------------
    # feedback
    get_feedback_avoirs(df, feedback)
    # suppression
    df = without_avoirs(df)
    # -------------------------------------------------

    # ------------ gestion des stock codes ---------------
    # feedback
    get_feedback_stock_codes(df, stock_codes_invalides, feedback)
    # suppression
    for stock_code in stock_codes_invalides:
        df = without_produit(df, stock_code)
    # -------------------------------------------------

    return {
        "data_frame": df,
        "feedback": feedback
    }
