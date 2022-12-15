from .outils import *

def get_pourcentage(nombre_lignes, feedback):
    pourcentage_exact = (100 * nombre_lignes) / feedback["nombre_enregistrements"]

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

def get_feedback_vouchers(df, feedback):
    nombre_lignes = nombre_gifts(df)

    feedback["etapes"].append({
        "nom": "suppression des vouchers",
        "critère": "StockCode commence par 'gift_'",
        "nombre lignes supprimées": nombre_lignes,
        "nombre lignes après suppression": get_nb_lignes_apres_supp(df, nombre_lignes),
        "pourcentage global": get_pourcentage(nombre_lignes, feedback)
    })

def get_feedback_pays(df, liste_pays, feedback):
    pd_serie = mask_pays(df, liste_pays).value_counts()
    nombre_lignes = pd_serie["autre"]

    feedback["etapes"].append({
        "nom": "regroupement des pays invalides sous un label `autre`",
        "critère": "Country ne faisant pas partie de la liste des pays valides",
        "nombre lignes modifiées": nombre_lignes,
        "nombre lignes après modification": df.shape[0],
        "pourcentage global": get_pourcentage(nombre_lignes, feedback)
    })

def nettoyage(fichier):
    # --------------- variables -----------------------
    feedback = {
        "nombre_enregistrements": 0,
        "etapes": []
    }
    subset = ["InvoiceNo", "StockCode"]
    stock_codes_invalides = ["S", "POST", "M", "DOT", "D", "BANK CHARGES", "AMAZONFEE"]
    liste_pays = [
        "United Kingdom",
        "Germany",
        "France",
        "EIRE",
        "Netherlands",
        "Spain",
        "Belgium",
        "Switzerland",
        "Australia",
        "Portugal",
        "Norway",
        "Cyprus",
        "Italy",
        "Finland",
        "Japan",
        "Hong Kong",
        "Sweden",
        "Poland",
        "Denmark",
        "Austria",
        "Singapore",
        "Iceland",
        "Greece",
        "Canada",
        "Malta",
        "Lebanon",
        "Israel",
        "Lithuania",
        "Brazil",
        "European Community",
        "United Arab Emirates",
        "USA",
        "Bahrain",
        "Czech Republic",
        "Saudi Arabia"
    ]
    # -------------------------------------------------

    # get data frame
    df = data_frame(fichier)

    # set nombre enregistrements
    feedback["nombre_enregistrements"] = df.shape[0]
    
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

    # ------------ gestion des vouchers ---------------
    # feedback
    get_feedback_vouchers(df, feedback)
    # suppression
    df = without_gifts(df)
    # -------------------------------------------------

    # ------------ gestion des pays ---------------
    # feedback
    get_feedback_pays(df, liste_pays, feedback)
    # modification
    df.loc[~df["Country"].isin(liste_pays), "Country"] = "autre"
    # -------------------------------------------------

    return {
        "data_frame": df,
        "feedback": feedback
    }
