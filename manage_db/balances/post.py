import sys
import logging

import pandas as pd
import requests

from manage_db.utils import batch_dataframe, time_operation


PICKLE_FILE = sys.argv[1]
API_URL = sys.argv[2]
N_BATCHES = 30


def balance_dict(row):
    return {
        'id': row['id'],
        'compte': row['compte'],
        'fonction_id': row['fonction_id'],
        'aggregat_depenses_id': row['aggregat_depenses_id'],
        'oobdeb': row['oobdeb'],
        'oobcre': row['oobcre'],
        'sd': row['sd'],
        'sc': row['sc'],
        'obnetdeb': row['obnetdeb'],
        'obnetcre': row['obnetcre'],
        'depense': row['depense']
    }


def depenses_aggregees_dict(row):
    return {
        'fonction_id': row['fonction_id'],
        'aggregat_depenses_id': row['aggregat_depenses_id'],
        'depenses_somme': row['depenses_somme']
    }


@time_operation
def aggregate_depenses(df):
    agg_df = (
        df
        .groupby(['code_insee', 'exercice', 'fonction_id', 'aggregat_depenses_id'])
        .agg({'depense': 'sum'})
        .rename(columns={'depense': 'depenses_somme'})
        .reset_index()
    )
    # garder uniquement les dépenses
    agg_df = agg_df[agg_df['aggregat_depenses_id'] != -1]
    return agg_df


def grouper_depenses_aggregees(df):
    """
    Groupement des dépenses aggrégées par budget

    :param df: pd.DataFrame contenant les dépenses aggrégées sous forme de dictionnaire
    :return: pd.DataFrame groupant les balances
    """
    def group_depenses(grouped):
        return pd.Series({'depenses_aggregees': list(grouped['depenses_aggregees_dict'])})

    return (
        df
        .groupby(['code_insee', 'exercice'])
        .apply(group_depenses)
        .reset_index()
    )


def grouper_balances(df):
    """
    Groupement des balances par budget

    :param df: pd.DataFrame contenant les balances sous forme de dictionnaire
    :return: pd.DataFrame groupant les balances
    """
    def group_balances(grouped):
        return pd.Series({'balances': list(grouped['balance_dict'])})

    return (
        df
        .groupby(['code_insee', 'exercice'])
        .apply(group_balances)
        .reset_index()
    )


@time_operation
def post_budgets(budgets):
    """
    Envoie les budgets, avec balances et les dépenses aggrégées, vers le backend via l'API.

    :param budgets: pd.DataFrame contenant les données
    """
    budgets_data = budgets.to_dict(orient='records')
    for data in budgets_data:
        code_insee = data.pop('code_insee')
        exercice = data.pop('exercice')
        response = requests.post(f'{API_URL}/budgets/{code_insee}/{exercice}', json=data)
        if response.status_code != 201:
            logging.debug(f"Error for {code_insee}: {response.content}")


def main():
    logging.basicConfig(filename='manage_db/.logs/post_balances.log', level=logging.DEBUG)

    # lecture et batching
    df = pd.read_pickle(PICKLE_FILE)
    df_batches = batch_dataframe(df, 'code_insee', N_BATCHES)

    for i, batch in enumerate(df_batches):

        print(f"*** Sending batch {i} of {N_BATCHES}")

        # groupement des dépenses aggrégées
        agg_batch = aggregate_depenses(batch)
        agg_batch['depenses_aggregees_dict'] = agg_batch.apply(depenses_aggregees_dict, axis=1)
        depenses_aggregees = grouper_depenses_aggregees(agg_batch)

        # groupement des balances
        batch['balance_dict'] = batch.apply(balance_dict, axis=1)
        balances = grouper_balances(batch)

        # poster les budgets
        budgets = depenses_aggregees.merge(balances, on=['code_insee', 'exercice'])
        post_budgets(budgets)


if __name__ == "__main__":
    main()
