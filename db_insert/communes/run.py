import sys

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_insert.models import CommuneModel, Base
from db_insert.utils import time_operation


DATAFILE_NOM = sys.argv[1]
DATAFILE_POP = sys.argv[2]
DATABASE = "sqlite:///app/data.db"


@time_operation
def main(db_session):
    # read and process insee file
    df_nom = pd.read_csv(
        filepath_or_buffer=DATAFILE_NOM,
        sep=',',
        encoding="utf-8",
        dtype=str,
        na_filter=False,
        usecols=['libelle', 'com', 'typecom']
    )
    df_nom = df_nom.rename(columns={'libelle': 'nom', 'com': 'code_insee'})
    df_nom = df_nom[df_nom['typecom'] == 'COM']
    df_nom = df_nom[['nom', 'code_insee']]

    # read and process population file
    df_pop = pd.read_csv(
        filepath_or_buffer=DATAFILE_POP,
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

    # create table and insert data

    communes = df.apply(CommuneModel.init_from_row, axis=1).values

    db_session.bulk_save_objects(communes, return_defaults=True)
    db_session.commit()
    return db_session


if __name__ == "__main__":
    # startup db engine and db session
    engine = create_engine(DATABASE, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # process files, save objects and close session
    session = main(session)
    session.close()
