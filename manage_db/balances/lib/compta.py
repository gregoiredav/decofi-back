from functools import reduce
from manage_db.compta import AGGREGATS_COMPTE_DEPENSES, MODES_DE_CALCUL_DEPENSES

import pandas as pd


def creer_aggregat_depenses_id(ligne):
    for code, aggregat in AGGREGATS_COMPTE_DEPENSES.items():
        comptes_a_inclure = aggregat['comptes_a_inclure']
        comptes_a_exclure = aggregat['comptes_a_exclure']
        if flag_aggregat_depenses(ligne, comptes_a_inclure, comptes_a_exclure):
            return code
    return -1


def flag_aggregat_depenses(ligne, a_inclure, a_exclure):
    flag = False
    for compte in a_inclure:
        if ligne.startswith(compte):
            flag = True
    for compte in a_exclure:
        if ligne.startswith(compte):
            flag = False
    return flag


def calcul_depenses_par_aggregat(df):
    """
    Calcule la dépense sur un compte en utilisant le bon mode de calcul pour cet aggrégat de dépense
    """
    modes_de_calcul = MODES_DE_CALCUL_DEPENSES(df)
    for mode_de_calcul in modes_de_calcul:
        aggregats_id = mode_de_calcul['aggregats_id']
        calcul_depenses = mode_de_calcul['calcul']
        df.loc[df['aggregat_depenses_id'].isin(aggregats_id), 'depense'] = calcul_depenses
    return df


def flag_vote_par_nature(df):
    """
    Détecte les collectivités qui votent par nature, signalées par des codes fonctions qui:
        - commencent par 9
        - dont la longueur est au moins 3 caractères

    :param df: pd.DataFrame issu du csv, après nettoyage et changements de noms
    :return: pd.DataFrame contenant les flags
    """
    df['aggregat_fonction'] = df['fonction'].apply(_aggregat_fonction)
    grouped = (
        df
        .groupby('code_insee')
        .apply(_custom_aggregation)
        .reset_index()
    )
    vote_par_nature = (
        True
        & (grouped['fonction_min_length'] >= 3)
        & (
                (grouped['aggregat_set'] == {9}) |
                (grouped['aggregat_set'] == {0, 9})
        )
    )
    grouped['vote_par_nature'] = vote_par_nature
    return grouped[['code_insee', 'vote_par_nature']]


def correction_vote_par_nature(code_fonction):
    """
    Retire le 9 en tête du code fonction pour les budgets votés par nature,
    afin d'obtenir l'équivalent du code fonction des budgets votés par fonction.

    :param code_fonction: code fonction issu de la nomenclature budgétaire (str)
    :return: code (str)
    """
    return code_fonction[2:]


def _custom_aggregation(df):
    names = {
        'fonction_min_length': _series_min_length(df['fonction']),
        'aggregat_set': _series_to_set(df['aggregat_fonction']),
    }
    return pd.Series(names)


def _aggregat_fonction(fonction):
    return int(fonction[0])


def _series_min_length(series):
    return reduce(lambda x, y: min(x, y), map(len, series))


def _series_to_set(series):
    return set(series)
