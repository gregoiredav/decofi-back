from app import db


class BalanceModel(db.Model):
    __tablename__ = 'balances'

    id = db.Column(db.Integer, primary_key=True, index=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), index=True)
    compte = db.Column(db.String(10))
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonctions.id'))
    sd = db.Column(db.Float(precision=2))
    sc = db.Column(db.Float(precision=2))
    oobdeb = db.Column(db.Float(precision=2))
    oobcre = db.Column(db.Float(precision=2))
    obnetdeb = db.Column(db.Float(precision=2))
    obnetcre = db.Column(db.Float(precision=2))
    aggregat_comptes_id = db.Column(db.Integer, db.ForeignKey('aggregats_comptes.id'))
    depenses = db.Column(db.Float(precision=2))
    fonction = db.relationship('FonctionModel', lazy='select')
    aggregats_comptes = db.relationship('AggregatComptesModel', lazy='select')

    def json(self):
        return {
            'id': self.id,
            'budget_id': self.budget_id,
            'compte': self.compte,
            'aggregat_comptes': self.aggregats_comptes.json(),
            'fonction': self.fonction.json(),
            'sd': self.sd,
            'sc': self.sc,
            'oobdeb': self.oobdeb,
            'oobcre': self.oobcre,
            'obnetdeb': self.obnetdeb,
            'obnetcre': self.obnetcre,
            'depenses': self.depenses,
        }

    @classmethod
    def find_unique(cls, collectivite_id, exercice, compte, fonction):
        return (
            cls.query
            .filter_by(
                collectivite_id=collectivite_id,
                exercice=exercice,
                compte=compte,
                fonction=fonction
            )
            .first()
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
