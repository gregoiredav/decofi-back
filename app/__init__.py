import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()


def create_app():
    # Initializing core application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'quelquechose'

    # Initializing plugins
    db.init_app(app)
    api = Api(app)

    #

    # Registering resources
    from app.resources.balance import Balance
    from app.resources.budget import Budget
    from app.resources.collectivite import Collectivite
    from app.resources.commune import CommuneList

    api.add_resource(Balance, '/balances/<int:_id>')
    api.add_resource(Budget, '/budgets/<int:_id>')
    api.add_resource(Collectivite, '/collectivites/<string:code_insee>')
    api.add_resource(CommuneList, '/communes')

    return app
