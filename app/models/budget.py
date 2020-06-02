from app import db


class AggregatDepensesModel(db.Model):
    __tablename__ = "aggregats_depenses"

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'))
    aggregat_comptes_id = db.Column(db.Integer, db.ForeignKey('aggregats_comptes.id'))
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonctions.id'))
    depenses = db.Column(db.Float(precision=2))
    fonction = db.relationship('FonctionModel', lazy='select')
    aggregat_comptes = db.relationship('AggregatComptesModel', lazy='select')

    def json(self):
        return {
            'budget_id': self.budget_id,
            'depenses': self.depenses,
            'aggregat_comptes': self.aggregat_comptes.json(),
            'fonction': self.fonction.json(),
        }


class BudgetModel(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    exercice = db.Column(db.Integer, index=True)
    code_insee = db.Column(db.Integer, db.ForeignKey('collectivites.code_insee'), index=True)
    balances = db.relationship('BalanceModel', lazy='dynamic')
    aggregats_depenses = db.relationship('AggregatDepensesModel', lazy='dynamic')

    def json(self, return_aggregates=True, return_balances=False):
        payload = {
            'id': self.id,
            'code_insee': self.code_insee,
            'exercice': self.exercice,
        }
        if return_aggregates:
            payload['aggregats_depenses'] = [balance.json() for balance in self.aggregats_depenses]
        if return_balances:
            payload['balances'] = [balance.json() for balance in self.balances]
        return payload

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_collectivite_and_year(cls, collectivite_id, annee):
        return (
            cls.query
            .filter_by(collectivite_id=collectivite_id, annee=annee)
            .first()
        )
