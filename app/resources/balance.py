from flask_restful import Resource, reqparse

from app.models.balance import BalanceModel


class Balance(Resource):

    @staticmethod
    def get(_id):

        balance = BalanceModel.query.get(_id)
        print(balance.aggregats_comptes.libelle)
        if not balance:
            return {"message", "Il n'existe pas balance avec ces paramètres de recherche."}, 204

        return balance.json()
