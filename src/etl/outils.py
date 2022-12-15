import pandas as pd
import numpy as np
import re

def data_frame(nom_fichier):
    return pd.read_csv(nom_fichier, encoding="iso-8859-1")

def is_negative(nombre):
    return nombre <= 0

def commence(sub_chars, chars):
    return False if re.search("^{}".format(sub_chars), chars) == None else True

def is_avoir(quantite):
    return "avoir" if is_negative(quantite) else "vente"

def is_gift(stock_code):
    return "gift" if commence("gift_", stock_code) else "autre"

def without_avoirs(data_frame):
    return data_frame[~(is_negative(data_frame["Quantity"]))]

def without_produit(data_frame, valeur):
    return data_frame[data_frame["StockCode"] != valeur]

def without_gifts(data_frame):
    return data_frame[~(data_frame["StockCode"].str.match("^gift_"))]

def mask_doublons(data_frame, subset):
    serie = data_frame.duplicated(subset=subset)

    return serie.map({False: "unique", True: "doublon"})

def mask_avoirs(data_frame):
    return data_frame["Quantity"].map(is_avoir)

def mask_produit(data_frame, valeur):
    return data_frame["StockCode"].map(lambda x : valeur if x == valeur else "autre")

def mask_gifts(data_frame):
    return data_frame["StockCode"].map(is_gift)

def mask_pays(data_frame, pays):
    return data_frame["Country"].map(lambda x : "LPDR" if x in pays else "autre")

def nombre_produits(df, valeur):
    try:
        return mask_produit(df, valeur).value_counts()[valeur]
    except:
        return 0

def nombre_gifts(df):
    try:
        return mask_gifts(df).value_counts()["gift"]
    except:
        return 0

def nombre_pays(df, valeur):
    try:
        return df["Country"].map(lambda x : valeur if x == valeur else "autre").value_counts()[valeur]
    except:
        return 0

def formate(pourcentage_lignes):
    return "{} %".format(round(pourcentage_lignes, 1))

def est_nat(date):
    return "nat" if np.isnat(np.datetime64(str(date))) else "date valide"

def mask_nat(data_frame):
    return data_frame["InvoiceDate"].map(est_nat)

def nombre_nat(df):
    try:
        return mask_nat(df).value_counts()["nat"]
    except:
        return 0
