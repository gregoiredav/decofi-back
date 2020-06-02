from app import db


class FonctionModel(db.Model):
    __tablename__ = "fonctions"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(255))

    def json(self):
        return {"id": self.id, "libelle": self.libelle}


class AggregatComptesModel(db.Model):
    __tablename__ = "aggregats_comptes"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(255))

    def json(self):
        return {"id": self.id, "libelle": self.libelle}
