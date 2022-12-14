from .outils import *

def get_pourcentage(nombre_lignes, feedback):
    pourcentage_exact = (100 * nombre_lignes) / feedback["nombre enregistrements"]

    return formate(pourcentage_exact) if pourcentage_exact >= 0.01 else "< 0.01 %"

def get_feedback_doublons(df, subset, feedback):
    pd_serie = mask_doublons(df, subset).value_counts()
    nombre_lignes = pd_serie["doublon"]

    feedback["etapes"].append({
        "nom": "suppression des doublons",
        "critère": "InvoiceNo et StockCode identiques",
        "nombre lignes": df.shape[0],
        "nombre lignes supprimées": nombre_lignes,
        "pourcentage global": get_pourcentage(nombre_lignes, feedback)
    })

def nettoyage(fichier):
    # --------------- variables -----------------------
    feedback = {
        "nombre enregistrements": 0,
        "etapes": []
    }
    subset = ["InvoiceNo", "StockCode"]
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

    return {
        "data_frame": df,
        "feedback": feedback
    }
