from app import db


class CollectiviteModel(db.Model):

    __tablename__ = 'collectivites'

    code_insee = db.Column(db.String(5), primary_key=True)
    budgets = db.relationship('BudgetModel', lazy='dynamic')

    def json(self, include_budgets=False):
        payload = {
            'code_insee': self.code_insee,
        }
        if include_budgets:
            payload['budgets'] = [budget.json() for budget in self.budgets]
        return payload
