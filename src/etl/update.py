from .outils_bdd import get_engine

def add_pays(bdd_engine):
    pays_df_nettoyes = """
        SELECT country
            FROM df_nettoye
    """
    pays_bdd = """
        SELECT country
            FROM pays
    """
    new_pays = """
        SELECT country FROM ({}) AS pays_df_nettoyes
        EXCEPT
        SELECT country FROM ({}) AS pays_bdd
    """.format(pays_df_nettoyes, pays_bdd)
    requete = """
        INSERT INTO pays (country)
        SELECT country FROM ({}) AS new_pays;
    """.format(new_pays)

    bdd_engine.execute(requete)

def add_produits(bdd_engine):
    produits_df_nettoyes = """
        SELECT stock_code
            FROM df_nettoye
    """
    produits_bdd = """
        SELECT stock_code
            FROM produit
    """
    new_produits = """
        SELECT stock_code FROM ({}) AS produits_df_nettoyes
        EXCEPT
        SELECT stock_code FROM ({}) AS produits_bdd
    """.format(produits_df_nettoyes, produits_bdd)
    requete = """
        INSERT INTO produit (stock_code)
        SELECT stock_code FROM ({}) AS new_produits;
    """.format(new_produits)

    bdd_engine.execute(requete)

def add_commandes(bdd_engine):
    commandes_df_nettoyes = """
        SELECT invoice_no, country
            FROM df_nettoye
    """
    commandes_bdd = """
        SELECT invoice_no, country_id
            FROM commande
    """
    new_commandes = """
        SELECT invoice_no, country FROM ({}) AS commandes_df_nettoyes
        EXCEPT
        SELECT invoice_no, country_id FROM ({}) AS commandes_bdd
    """.format(commandes_df_nettoyes, commandes_bdd)
    requete = """
        INSERT INTO commande (invoice_no, country_id)
        SELECT invoice_no, country FROM ({}) AS new_commandes;
    """.format(new_commandes)

    bdd_engine.execute(requete)

def update_bdd():
    bdd_engine = get_engine()
    # ajouter pays
    add_pays(bdd_engine)
    # ajouter produits
    add_produits(bdd_engine)
    # ajouter commandes
    add_commandes(bdd_engine)
    # ajouter details commandes
