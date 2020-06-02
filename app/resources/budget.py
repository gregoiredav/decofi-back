from flask_restful import Resource, reqparse

from app.models.budget import BudgetModel


class Budget(Resource):

    @staticmethod
    def get(_id):
        budget = BudgetModel.query.get(_id)
        return budget.json(return_aggregates=False, return_balances=True)