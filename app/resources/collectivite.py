from flask_restful import Resource

from app.models.collectivite import CollectiviteModel


class Collectivite(Resource):

    @staticmethod
    def get(code_insee):

        collectivite = CollectiviteModel.query.get(code_insee)

        if not collectivite:
            return {"message": "Collectivite introuvable."}

        return collectivite.json(include_budgets=True)