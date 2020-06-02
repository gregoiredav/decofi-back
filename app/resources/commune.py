from flask import request
from flask_restful import Resource
from app.models.commune import CommuneModel


class CommuneList(Resource):

    max_records = 100

    @classmethod
    def get(cls):
        query_string = request.args.get('inputValue', None)
        if query_string:
            communes = CommuneModel.match_name(query_string, max_records=cls.max_records)
        else:
            communes = CommuneModel.query.limit(cls.max_records).all()
        return [commune.json() for commune in communes]

# class Commune(Resource):
# 
#     
