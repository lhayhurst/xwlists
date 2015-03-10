__author__ = 'lhayhurst'

import json
from flask import jsonify
import myapp
from persistence import PersistenceManager
from flask.ext import restful
from flask.ext.restful import reqparse

RESULT = 'result'
PLAYER2_POINTS = 'player2points'
PLAYER1_POINTS = 'player1points'
PLAYER2 = 'player2'
PLAYER1 = 'player1'
MATCHES = 'matches'
ROUND_NUMBER = 'round-number'
ROUND_TYPE = 'round-type'
ROUNDS = 'rounds'
ELIMINATION = 'elimination'
SWISS = 'swiss'
RANK = 'rank'
SOS = 'sos'
MOV = 'mov'
SCORE = 'score'
PLAYER_NAME = 'name'
PLAYERS = "players"
ROUND_LENGTH = "round_length"
TYPE = "type"
DATE = "date"
NAME = "name"
ID = "id"
TOURNAMENT = "tournament"



class Tournaments(restful.Resource):

    def get(self):
        pm = PersistenceManager(myapp.db_connector)
        ids = pm.get_tourney_ids()
        ret = []
        for id in ids:
            ret.append(id[0])
        return json.dumps({ 'tournaments' : ret } )


class TourneyToJsonConverter:
    def convert(self, t):
        tournament = {}
        ret = {}
        ret[TOURNAMENT] = tournament
        tournament[ID] = t.id
        tournament[NAME] = t.tourney_name
        tournament[DATE] = str(t.tourney_date)
        tournament[TYPE] = t.tourney_type
        tournament[ROUND_LENGTH] = t.round_length

        #build the tournament to ranking map
        #naive assumption: assume the rankings are there
        players = []
        tournament[PLAYERS] = players
        for ranking in t.rankings:
            player = {}
            player[PLAYER_NAME] = ranking.player.player_name
            player[SCORE] = ranking.score
            player[MOV] = ranking.mov
            player[SOS] = ranking.sos
            rank = {}
            player[RANK] = rank
            rank[SWISS] = ranking.rank
            if ranking.elim_rank is not None:
                rank[ELIMINATION] = ranking.elim_rank
            players.append( player)

        #and now the rounds
        rounds = []
        tournament[ROUNDS] = rounds
        for round in t.rounds:
            rhref = {}
            rounds.append(rhref)
            rhref[ROUND_TYPE] = round.round_type_str()
            rhref[ROUND_NUMBER] = round.round_num
            matches = []
            rhref[MATCHES] = matches
            for result in round.results:
                resref = {}
                matches.append(resref)
                resref[PLAYER1] = result.player1_name()
                resref[PLAYER2] = result.player2_name()
                resref[PLAYER1_POINTS] = result.list1_score
                resref[PLAYER2_POINTS] = result.list2_score
                resref[RESULT] = result.get_result_for_json()

        return json.dumps(ret)

class Tournament(restful.Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('json', type=str, help='Rate to charge for this resource')
        args = self.parser.parse_args()
    def get(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        t = pm.get_tourney_by_id(tourney_id)
        if t is None:
            response = jsonify(message="tourney %d not found" % ( tourney_id ))
            response.status_code = 404
            return response
        return TourneyToJsonConverter().convert(t)

    # def post(self, tourney_id):
    #     args = self.parser.parse_args()
    #     print args.get('json')
    #     t    = json.loads( args.get( 'json '))
    #     print t
