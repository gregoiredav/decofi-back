from app import db


class BalanceModel(db.Model):
    __tablename__ = 'balances'

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.String(20), db.ForeignKey('budgets.id'), index=True)
    compte = db.Column(db.String(20))
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonctions.id'))
    sd = db.Column(db.Float(precision=2))
    sc = db.Column(db.Float(precision=2))
    oobdeb = db.Column(db.Float(precision=2))
    oobcre = db.Column(db.Float(precision=2))
    obnetdeb = db.Column(db.Float(precision=2))
    obnetcre = db.Column(db.Float(precision=2))
    aggregat_depenses_id = db.Column(db.Integer, db.ForeignKey('aggregats_depenses.id'))
    depense = db.Column(db.Float(precision=2))

    fonction = db.relationship('FonctionModel', lazy='select')
    aggregat_depenses = db.relationship('AggregatDepensesModel', lazy='select')

    def __init__(self, code_insee, exercice, **data):
        self.budget_id = '_'.join([code_insee, str(exercice)])
        self.compte = data['compte']
        self.aggregat_depenses_id = data['aggregat_depenses_id']
        self.fonction_id = data['fonction_id']
        self.sd = data['sd']
        self.sc = data['sc']
        self.oobdeb = data['oobdeb']
        self.oobcre = data['oobcre']
        self.obnetdeb = data['obnetdeb']
        self.obnetcre = data['obnetcre']
        self.depense = data['depense']

    def json(self):
        return {
            'id': self.id,
            'budget_id': self.budget_id,
            'compte': self.compte,
            'aggregat_depenses_id': self.aggregat_depenses_id,
            'fonction_id': self.fonction_id,
            'sd': self.sd,
            'sc': self.sc,
            'oobdeb': self.oobdeb,
            'oobcre': self.oobcre,
            'obnetdeb': self.obnetdeb,
            'obnetcre': self.obnetcre,
            'depense': self.depense,
        }
