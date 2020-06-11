import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from manage_db.compta import LIBELLES_FONCTIONS, AGGREGATS_COMPTE_DEPENSES


DATABASE = os.getenv("DATABASE_URL", "sqlite:///app/data.db")

Base = declarative_base()


class AggregatDepensesModel(Base):
    __tablename__ = "aggregats_depenses"

    id = Column(Integer, primary_key=True)
    libelle = Column(String(255))

    def __init__(self, _id, libelle):
        self.id = _id
        self.libelle = libelle


class FonctionModel(Base):
    __tablename__ = "fonctions"

    id = Column(Integer, primary_key=True)
    libelle = Column(String(255))

    def __init__(self, _id, libelle):
        self.id = _id
        self.libelle = libelle


engine = create_engine(DATABASE)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# fonctions
fonction_objects = [FonctionModel(_id, libelle) for _id, libelle in LIBELLES_FONCTIONS.items()]
session.add_all(fonction_objects)
session.commit()

# aggregats
aggregats_objects = [AggregatDepensesModel(_id, aggregat['libelle']) for _id, aggregat in
                     AGGREGATS_COMPTE_DEPENSES.items()]
session.add_all(aggregats_objects)
session.commit()

session.close()




