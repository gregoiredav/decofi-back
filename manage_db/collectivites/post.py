import sys
import logging

import requests
import pandas as pd

from manage_db.utils import time_operation


@time_operation
def process_csv_data(insee_codes_fp, insee_population_fp):
    """
    Lecture des csv de l'INSEE pour rassembler les données à poster vers l'API.

    :return: pd.DataFrame contenant l'information sur les collectivités
    """
    df_nom = pd.read_csv(
        filepath_or_buffer=insee_codes_fp,
        sep=',',
        encoding="utf-8",
        dtype=str,
        na_filter=False,
        usecols=['libelle', 'com', 'typecom']
    )
    df_nom = df_nom.rename(columns={'libelle': 'nom', 'com': 'code_insee', 'typecom': 'sous_categorie'})
    df_nom = df_nom[['nom', 'code_insee', 'sous_categorie']]
    df_nom['categorie'] = 'Commune'

    # read and process population file
    df_pop = pd.read_csv(
        filepath_or_buffer=insee_population_fp,
        sep=';',
        encoding="utf-8",
        dtype=str,
        na_filter=False,
        usecols=['DEPCOM', 'PTOT'],

    )
    df_pop = df_pop.rename(columns={'DEPCOM': 'code_insee', 'PTOT': 'population'})
    df_pop['population'] = df_pop['population'].apply(int)

    # merge nom and pop
    df = df_nom.merge(df_pop, how='left', on='code_insee').sort_values(by='population', ascending=False)
    df.fillna(-1, inplace=True)
    return df[['code_insee', 'categorie', 'sous_categorie', 'nom', 'population']]


@time_operation
def upsert_collectivites(collectivites, api_url):
    """
    Charge les collectivités dans la base de donnée via des requêtes PUT.

    :param collectivites: list(dict) contenant les données de chaque collectivité
    """
    for collectivite in collectivites:
        data = collectivite.copy()
        code_insee = data.pop('code_insee')
        response = requests.put(f'{api_url}/collectivites/{code_insee}', json=data)
        if response.status_code != 201:
            logging.debug(f"Error for {code_insee}: {response.content}")


def main(insee_codes_fp, insee_population_fp, api_url):
    logging.basicConfig(filename='manage_db/.logs/post_collectivites.log', level=logging.DEBUG)

    df = process_csv_data(insee_codes_fp, insee_population_fp)
    collectivites = df.to_dict(orient='records')
    upsert_collectivites(collectivites, api_url)


if __name__ == "__main__":
    INSEE_CODE_FP = sys.argv[1]
    INSEE_POPULATION_FP = sys.argv[2]
    API_URL = sys.argv[3]
    main(INSEE_CODE_FP, INSEE_POPULATION_FP, API_URL)
