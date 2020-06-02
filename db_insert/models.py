from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class CollectiviteModel(Base):
    __tablename__ = 'collectivites'

    code_insee = Column(String(5), index=True, primary_key=True)
    budgets = relationship('BudgetModel', lazy='dynamic')

    def __repr__(self):
        return f"<Collectivite(code_insee={self.code_insee})>"

    def __init__(self, code_insee):
        self.code_insee = code_insee


class BudgetModel(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    exercice = Column(Integer, index=True)
    code_insee = Column(String(5), ForeignKey('collectivites.code_insee'), index=True)
    balances = relationship('BalanceModel', lazy='dynamic')
    aggregats_depenses = relationship('AggregatDepensesModel', lazy='dynamic')
    
    def __repr__(self):
        return f"<Budget(exercice={self.exercice})>"

    @classmethod
    def init_from_row(cls, row):
        return cls(
            exercice=row['exercice'],
            code_insee=row['code_insee'],
            balances=row['balances'],
            aggregats_depenses=row['aggregats_depenses'],
        )


class BalanceModel(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'), index=True)
    compte = Column(String(10))
    fonction_id = Column(Integer, ForeignKey('fonctions.id'))
    sd = Column(Float(precision=2))
    sc = Column(Float(precision=2))
    oobdeb = Column(Float(precision=2))
    oobcre = Column(Float(precision=2))
    obnetdeb = Column(Float(precision=2))
    obnetcre = Column(Float(precision=2))
    aggregat_comptes_id = Column(Integer, ForeignKey('aggregats_comptes.id'))
    depenses = Column(Float(precision=2))

    def __repr__(self):
        return f"<Balance(compte={self.compte}, fonction={self.compte})>"

    @classmethod
    def init_from_row(cls, row):
        return cls(
            compte=row['compte'],
            fonction_id=row['fonction_id'],
            oobdeb=row['oobdeb'],
            oobcre=row['oobcre'],
            sd=row['sd'],
            sc=row['sc'],
            obnetcre=row['obnetcre'],
            obnetdeb=row['obnetdeb'],
            aggregat_comptes_id=row['aggregat_comptes_id'],
            depenses=row['depenses'],
        )


class CommuneModel(Base):
    __tablename__ = 'communes'

    code_insee = Column(String(5), primary_key=True)
    nom = Column(String(100), index=True)
    population = Column(Integer)

    def __repr__(self):
        return f'<Commune(code_commune={self.code_insee})>'

    @classmethod
    def init_from_row(cls, row):
        return cls(
            code_insee=row['code_insee'],
            nom=row['nom'],
            population=row['population']
        )


class AggregatDepensesModel(Base):
    __tablename__ = "aggregats_depenses"

    id = Column(Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'))
    aggregat_comptes_id = Column(Integer, ForeignKey('aggregats_comptes.id'))
    fonction_id = Column(Integer, ForeignKey('fonctions.id'))
    depenses = Column(Float(precision=2))

    @classmethod
    def init_from_row(cls, row):
        return cls(
            aggregat_comptes_id=row['aggregat_comptes_id'],
            fonction_id=row['fonction_id'],
            depenses=row['depenses']
        )


class AggregatComptesModel(Base):
    __tablename__ = "aggregats_comptes"

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
