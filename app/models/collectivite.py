from app import db


class CollectiviteModel(db.Model):

    __tablename__ = 'collectivites'

    code_insee = db.Column(db.String(5), primary_key=True)
    categorie = db.Column(db.String(255), index=True)
    sous_categorie = db.Column(db.String(255))
    nom = db.Column(db.String(255), index=True)
    population = db.Column(db.Integer)

    budgets = db.relationship('BudgetModel', lazy='dynamic')

    def __init__(self, code_insee, categorie, sous_categorie, nom, population):
        self.code_insee = code_insee
        self.categorie = categorie
        self.sous_categorie = sous_categorie
        self.nom = nom
        self.population = population

    def json(self, include_budgets=False):
        payload = {
            'code_insee': self.code_insee,
            'categorie': self.categorie,
            'sous_categorie': self.sous_categorie,
            'nom': self.nom,
            'population': self.population,
        }
        if include_budgets:
            payload['budgets'] = [budget.json() for budget in self.budgets]
        return payload

    def update(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    @classmethod
    def match_name(cls, query_string, max_records):
        return (
            cls
            .query
            .filter(cls.nom.like(f"%{query_string}%"))
            .order_by(cls.population.desc())
            .limit(max_records)
            .all()
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
