from flask import request
from flask_restful import Resource

from app.models.collectivite import CollectiviteModel


class Collectivite(Resource):

    @staticmethod
    def get(code_insee):
        collectivite = CollectiviteModel.query.get(code_insee)
        if not collectivite:
            return {"message": "Collectivite introuvable."}
        return collectivite.json(include_budgets=True)

    @staticmethod
    def post(code_insee):
        collectivite = CollectiviteModel.query.get(code_insee)
        if collectivite:
            return {"message": "Il existe déjà une collectivité avec ce code INSEE"}, 400

        data = request.json
        collectivite = CollectiviteModel(code_insee=code_insee, **data)
        collectivite.save_to_db()
        return collectivite.json(), 201

    @staticmethod
    def put(code_insee):
        data = request.json
        collectivite = CollectiviteModel.query.get(code_insee)
        if collectivite:
            collectivite.update(**data)
        else:
            collectivite = CollectiviteModel(code_insee=code_insee, **data)
        collectivite.save_to_db()
        return collectivite.json(), 201
