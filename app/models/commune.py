from app import db


class CommuneModel(db.Model):

    __tablename__ = 'communes'

    code_insee = db.Column(db.String(5), primary_key=True)
    nom = db.Column(db.String(100), index=True)
    population = db.Column(db.Integer)

    def json(self):
        return {'code_insee': self.code_insee, 'nom': self.nom}

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
