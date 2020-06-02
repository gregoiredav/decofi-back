import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_insert.models import Base, CollectiviteModel
import db_insert.balances.lib.main as lib


DATAFILE = sys.argv[1]
CATEGORIES = ['Commune']
DATABASE = "sqlite:///app/data.db"
DATA_SPLITS = 30

engine = create_engine(DATABASE)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

df_all = lib.read_csv(DATAFILE)
df_all = lib.clean(df_all, categories=CATEGORIES)
df_all = lib.creer_aggregats_comptes(df_all)

codes_insee = df_all['code_insee'].unique()
collectivites = map(CollectiviteModel, codes_insee)
session = Session()
session.bulk_save_objects(collectivites)
session.commit()
session.close()


df_splits = lib.sort_and_split(df_all, DATA_SPLITS)

for i, df in enumerate(df_splits):
    print(f"*** Starting batch {i + 1} of {DATA_SPLITS} ***")
    agg_df = lib.create_aggregate_depenses_objects(df)
    agg_df = lib.group_aggregate_depenses_by_budget(agg_df)

    df = lib.vote_par_nature(df)
    df = lib.create_balance_objects(df)
    df = lib.group_balances_by_budget(df)

    df = df.merge(agg_df, on=['code_insee', 'exercice'])

    budgets = lib.create_budget_objects(df)

    lib.save_objects_to_db(Session, budgets)
