import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_insert.models import AggregatComptesModel, FonctionModel, Base
from db_insert.nomenclatures import LIBELLES_FONCTIONS, AGGREGATS_COMPTES


DATABASE = os.getenv("DATABASE_URL", "app/data.db")


engine = create_engine(DATABASE)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# fonctions
fonction_objects = [FonctionModel(_id, libelle) for _id, libelle in LIBELLES_FONCTIONS.items()]
session.add_all(fonction_objects)
session.commit()

# aggregats
aggregats_objects = [AggregatComptesModel(_id, aggregat['libelle']) for _id, aggregat in AGGREGATS_COMPTES.items()]
session.add_all(aggregats_objects)
session.commit()

session.close()




