from flask import request
from flask_restful import Resource

from app.models.budget import BudgetModel, DepenseAggregeeModel
from app.models.balance import BalanceModel


class Budget(Resource):

    @staticmethod
    def get(code_insee, exercice):
        budget_id = '_'.join([code_insee, str(exercice)])
        budget = BudgetModel.query.get(budget_id)
        if not budget:
            return {"message": "Ce budget n'existe pas dans la base de donnée"}, 404
        return budget.json(return_depenses_aggregees=True, return_balances=False)

    @staticmethod
    def post(code_insee, exercice):
        budget_id = '_'.join([code_insee, str(exercice)])
        budget = BudgetModel.query.get(budget_id)
        if budget:
            return {"message": "Il existe déjà un budget pour ce code INSEE et cet exercice"}, 400

        data = request.json

        balances_data = data['balances']
        balances = [BalanceModel(code_insee, exercice, **data) for data in balances_data]

        depenses_aggregees_data = data['depenses_aggregees']
        depenses_aggregees = [DepenseAggregeeModel(code_insee, exercice, **data) for data in depenses_aggregees_data]
        budget = BudgetModel(code_insee, exercice, balances, depenses_aggregees)
        budget.save_to_db()
        return budget.json(return_depenses_aggregees=True, return_balances=False), 201

    @staticmethod
    def delete(code_insee, exercice):
        budget_id = '_'.join([code_insee, str(exercice)])
        budget = BudgetModel.query.get(budget_id)
        if not budget:
            return {"message": "Ce budget n'existe pas dans la base de donnée"}, 400

        budget.delete_from_db()
        return {"message": "Ce budget a été supprimé"}, 200
