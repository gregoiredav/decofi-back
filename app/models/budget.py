from app import db


class DepenseAggregeeModel(db.Model):
    __tablename__ = "depenses_aggregees"

    id = db.Column(db.String(20), primary_key=True)
    budget_id = db.Column(db.String(20), db.ForeignKey('budgets.id'))
    aggregat_depenses_id = db.Column(db.Integer, db.ForeignKey('aggregats_depenses.id'))
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonctions.id'))
    depenses_somme = db.Column(db.Float)

    fonction = db.relationship('FonctionModel', lazy='select')
    aggregat_depenses = db.relationship('AggregatDepensesModel', lazy='select')

    def __init__(self, code_insee, exercice, **data):

        self.budget_id = '_'.join([code_insee, str(exercice)])
        self.id = '_'.join([self.budget_id, str(data['aggregat_depenses_id']), str(data['fonction_id'])])

        self.aggregat_depenses_id = data['aggregat_depenses_id']
        self.fonction_id = data['fonction_id']
        self.depenses_somme = data['depenses_somme']

    def json(self):
        return {
            'budget_id': self.budget_id,
            'depenses_somme': self.depenses_somme,
            'aggregat_depenses': self.aggregat_depenses.json(),
            'fonction': self.fonction.json(),
        }


class BudgetModel(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.String(20), primary_key=True)
    exercice = db.Column(db.Integer)
    code_insee = db.Column(db.String(20), db.ForeignKey('collectivites.code_insee'))

    balances = db.relationship('BalanceModel', lazy='select', cascade="all, delete-orphan")
    depenses_aggregees = db.relationship('DepenseAggregeeModel', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, code_insee, exercice, balances, depenses_aggregees):
        self.id = '_'.join([code_insee, str(exercice)])
        self.code_insee = code_insee
        self.exercice = exercice
        self.balances = balances
        self.depenses_aggregees = depenses_aggregees

    def json(self, return_depenses_aggregees=True, return_balances=False):
        payload = {
            'id': self.id,
            'code_insee': self.code_insee,
            'exercice': self.exercice,
        }
        if return_depenses_aggregees:
            payload['depenses_aggregees'] = [depense.json() for depense in self.depenses_aggregees]
        if return_balances:
            payload['balances'] = [balance.json() for balance in self.balances]
        return payload

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
