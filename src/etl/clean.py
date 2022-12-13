from .outils import *

feedback = {
    "nb_enregistrement": 0,
    "etapes": []
}
subset = ["InvoiceNo", "StockCode"]

def get_pourcentage(nombre_lignes):
    pourcentage_exact = (100 * nombre_lignes) / feedback["nb_enregistrement"]

    return formate(pourcentage_exact) if pourcentage_exact >= 0.01 else "< 0.01 %"

def supp_doublons(df):
    df.drop_duplicates(subset=subset, inplace=True)

def manage_doublons(df, subset):
    pd_serie = mask_doublons(df, subset).value_counts()
    nombre_lignes = pd_serie["doublon"]

    feedback["etapes"].append({
        "nom": "suppression des doublons",
        "critere": "InvoiceNo et StockCode identiques",
        "nombre_lignes": nombre_lignes,
        "pourcentage": get_pourcentage(nombre_lignes)
    })

    supp_doublons(df)

def nettoyer(fichier):
    df = data_frame(fichier)

    # set nb_enregistrements
    feedback["nb_enregistrement"] = df.shape[0]
    
    manage_doublons(df, subset)
