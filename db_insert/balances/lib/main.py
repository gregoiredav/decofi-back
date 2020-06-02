import pandas as pd
import numpy as np

from db_insert.models import BudgetModel, BalanceModel, AggregatDepensesModel
from db_insert.balances.lib.cleaner import Cleaner
from db_insert.balances.lib.compta import (flag_vote_par_nature, correction_vote_par_nature, creer_aggregat_id,
                                           calcul_depenses_par_aggregat)
from db_insert.utils import time_operation


@time_operation
def read_csv(file_path):
    return pd.read_csv(
        filepath_or_buffer=file_path,
        sep=';',
        encoding="ISO-8859-1",
        dtype=str,
        na_filter=False,
    )


@time_operation
def clean(df, categories):
    # filtrer les categories de collectivites
    df = df[df['CATEG'].isin(categories)]

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
    df['code_insee'] = df['ndept'] + df['insee']
    df['fonction_id'] = df['fonction'].apply(lambda fonction: int(fonction[0]))
    return df


@time_operation
def creer_aggregats_comptes(df):
    df.loc[:, 'aggregat_comptes_id'] = df['compte'].apply(creer_aggregat_id)
    df.dropna(subset=['aggregat_comptes_id'], inplace=True)
    df['aggregat_comptes_id'] = df['aggregat_comptes_id'].apply(int)
    # calculer les dépenses selon les aggrégats de compte
    df = calcul_depenses_par_aggregat(df)
    return df


@time_operation
def sort_and_split(df, nr_splits):
    df.sort_values(by='code_insee', inplace=True)
    code_insee_array = df['code_insee'].unique()
    code_insee_splits = np.array_split(code_insee_array, nr_splits)
    df_splits = map(lambda split: df[df['code_insee'].isin(split)], code_insee_splits)
    return list(df_splits)


@time_operation
def vote_par_nature(df):
    # Flag votes par nature et corriger l'aggrégat
    flags = flag_vote_par_nature(df)
    df = df.merge(flags, on='code_insee')

    mask = df['vote_par_nature']
    df.loc[mask, 'fonction'] = df.loc[mask, 'fonction'].apply(correction_vote_par_nature)
    return df


@time_operation
def create_aggregate_depenses_objects(df):
    agg_df = (
        df
        .groupby(['code_insee', 'exercice', 'fonction_id', 'aggregat_comptes_id'])
        .agg({'depenses': 'sum'})
        .reset_index()
    )
    init_cols = ['fonction_id', 'aggregat_comptes_id', 'depenses']
    agg_df.loc[:, 'aggregat_depenses'] = agg_df[init_cols].apply(AggregatDepensesModel.init_from_row, axis=1)
    return agg_df


@time_operation
def group_aggregate_depenses_by_budget(df):
    groupby_cols = ['code_insee', 'exercice']

    def aggregate_depenses(df):
        return pd.Series({'aggregats_depenses': list(df['aggregat_depenses'])})

    return df.groupby(groupby_cols).apply(aggregate_depenses).reset_index()


@time_operation
def create_balance_objects(df):
    init_cols = ['compte', 'fonction_id', 'oobdeb', 'oobcre', 'sd', 'sc', 'obnetcre', 'obnetdeb',
                 'aggregat_comptes_id', 'depenses']
    df.loc[:, 'balance'] = df[init_cols].apply(BalanceModel.init_from_row, axis=1)
    return df


@time_operation
def group_balances_by_budget(df):
    groupby_cols = ['code_insee', 'exercice']

    def aggregate_balances(df):
        return pd.Series({'balances': list(df['balance'])})

    return df.groupby(groupby_cols).apply(aggregate_balances).reset_index()


@time_operation
def create_budget_objects(df):
    init_cols = ['exercice', 'code_insee', 'balances', 'aggregats_depenses']
    return df[init_cols].apply(BudgetModel.init_from_row, axis=1).values


@time_operation
def save_objects_to_db(session_maker, objects):
    session = session_maker()
    session.add_all(objects)
    session.commit()
    session.close()
    return

