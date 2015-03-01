import json
import myapp
from persistence import PersistenceManager

__author__ = 'lhayhurst'

from flask.ext import restful

class Tournaments(restful.Resource):

    def get(self):
        pm = PersistenceManager(myapp.db_connector)
        ids = pm.get_tourney_ids()
        ret = []
        for id in ids:
            ret.append(id[0])
        return json.dumps(ret)


    def post(self):
        print "post"
        return {'hello': 'world'}

    def delete(self):
        print "delete"
        return {'hello': 'world'}

class Tournament(restful.Resource):
    def get(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        t = pm.get_tourney_by_id(tourney_id)
        tournament = {}
        ret["tournament"] = tournament
        tournament["id"] = t.id
        tournament["name"] = t.tourney_name
        tournament["date"] = t.tourney_date


        return {'hello': 'world'}