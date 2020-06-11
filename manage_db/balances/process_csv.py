import sys

import pandas as pd

from manage_db.utils import time_operation
from manage_db.balances.lib.cleaner import Cleaner
from manage_db.balances.lib.compta import (flag_vote_par_nature, correction_vote_par_nature, creer_aggregat_depenses_id,
                                           calcul_depenses_par_aggregat)

CSV_PATH = sys.argv[1]
PICKLE_PATH = sys.argv[2]
CATEGORIES = ['Commune']


@time_operation
def lecture_csv(file_path):
    return pd.read_csv(
        filepath_or_buffer=file_path,
        sep=';',
        encoding="ISO-8859-1",
        dtype=str,
        na_filter=False,
    )


@time_operation
def nettoyer_données(df):
    """
    Nettoie les données du csv, change les noms de colonnes.

    :param df: pandas DataFrame contenant les données brutes du csv
    :return: pandas DataFrame contenant les données nettoyées
    """
    # conserver les colonnes d'interets et passer leurs noms en minuscule
    df = df[['EXER', 'INSEE', 'FONCTION', 'COMPTE', 'NDEPT', 'OOBDEB', 'OOBCRE', 'SD', 'SC', 'OBNETDEB', 'OBNETCRE']]
    df = df.rename(lambda colname: colname.lower(), axis=1)
    df = df.rename(columns={'exer': 'exercice'})

    # Data cleaning
    cleaner = Cleaner({
        'exercice': int,
        'insee': Cleaner.insee,
        'fonction': Cleaner.fonction,
        'ndept': Cleaner.ndept,
        'oobdeb': Cleaner.chiffre,
        'oobcre': Cleaner.chiffre,
        'sd': Cleaner.chiffre,
        'sc': Cleaner.chiffre,
        'obnetdeb': Cleaner.chiffre,
        'obnetcre': Cleaner.chiffre,
    })
    df = cleaner.clean(df)
    return df


@time_operation
def creer_aggregats_de_depenses(df):
    # créer des aggrégats de comptes par type de dépenses
    df['aggregat_depenses_id'] = df['compte'].apply(creer_aggregat_depenses_id)
    # calculer les dépenses selon les aggrégats de compte
    df = calcul_depenses_par_aggregat(df)
    return df


@time_operation
def corriger_fonction(df):
    """
    Corrige le code fonction des budgets votés pas nature afin qu'ils soient comparable au code fonction des budgets
    votés par fonction.
    """
    flags = flag_vote_par_nature(df)
    df = df.merge(flags, on='code_insee')

    mask = df['vote_par_nature']
    df.loc[mask, 'fonction'] = df.loc[mask, 'fonction'].apply(correction_vote_par_nature)
    df['fonction_id'] = df['fonction'].apply(lambda fonction: int(fonction[0]))
    return df


def main():
    raw_df = lecture_csv(CSV_PATH)
    # filter les communes
    raw_df = raw_df[raw_df['CATEG'].isin(CATEGORIES)]
    clean_df = nettoyer_données(raw_df)
    # créer le code INSEE
    clean_df['code_insee'] = clean_df['ndept'] + clean_df['insee']
    df = creer_aggregats_de_depenses(clean_df)
    df = corriger_fonction(df)
    # créer une colonne id
    df.reset_index(inplace=True)
    df['id'] = df.apply(lambda row: '_'.join([str(row['exercice']), str(row['index'])]), axis=1)
    df.to_pickle(PICKLE_PATH)
    print(f"Pickle file sauvegardé au path suivant: {PICKLE_PATH}")


if __name__ == "__main__":
    main()
