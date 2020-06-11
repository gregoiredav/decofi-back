import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

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
    migrate = Migrate(app, db)

    # Registering resources
    from app.resources.budget import Budget
    from app.resources.collectivite import Collectivite

    api.add_resource(Budget, '/budgets/<string:code_insee>/<int:exercice>')
    api.add_resource(Collectivite, '/collectivites/<string:code_insee>')

    return app
