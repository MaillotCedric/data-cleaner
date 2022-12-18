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

def update_bdd():
    bdd_engine = get_engine()
    # ajouter pays
    add_pays(bdd_engine)
    # ajouter produits
    # ajouter commandes
    # ajouter details commandes
