DROPPED = 'dropped'
VENUE = 'venue'
__author__ = 'lhayhurst'

import json
from flask import jsonify, request
import myapp
from persistence import PersistenceManager, Tourney, TourneyVenue, TourneyPlayer, TourneyRanking, TourneyList
from flask.ext import restful
from flask.ext.restful import reqparse
import dateutil.parser

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
PARTICIPANT_COUNT = "participant_count"
TOURNAMENT = "tournament"
TOURNAMENTS = "tournaments"
CITY = 'city'
STATE = 'state'
COUNTRY = 'country'
VENUE = 'venue'
EMAIL = 'email'

class Tournaments(restful.Resource):

    def get(self):
        pm = PersistenceManager(myapp.db_connector)
        ids = pm.get_tourney_ids()
        ret = []
        for id in ids:
            ret.append(id[0])
        return json.dumps({ TOURNAMENTS : ret } )

    required_fields = [ NAME, DATE, TYPE, ROUND_LENGTH, PARTICIPANT_COUNT ]
    tourney_types   = [ "World Championship", "Nationals", "Regional", "Store Championship", "Vassal play",  "Other"]

    def missing_required_field(self, t):
        for rf in Tournaments.required_fields:
            if not t.has_key( rf ):
                return rf
        return None

    def four_oh_four(self, text):
        response = jsonify(message=text)
        response.status_code = 404
        return response
    def post(self):
        json_data = None
        try:
            json_data = request.get_json( force=True )
        except Exception:
            return self.four_oh_four( "bad json received!" )
        if json_data is not None:
            if json_data.has_key(TOURNAMENT):
                t = json_data[TOURNAMENT]

                email        = None
                sets_used = None
                rounds = None
                country = None
                city = None
                state = None
                venue = None

                #it should have all the required fields
                missing_field = self.missing_required_field(t)
                if missing_field is not None:
                    return self.four_oh_four("invalid tourney submission, must contain required fields, missing %s " % ( missing_field ))

                tourney_name      = t[ NAME ]
                tourney_date      = t[ DATE ]
                tourney_type      = t[ TYPE ]
                round_length      = t[ ROUND_LENGTH ]
                participant_count = t[PARTICIPANT_COUNT]

                #validate the tourney date
                parsed_date = None
                try:
                    parsed_date = dateutil.parser.parse( tourney_date )
                except Exception:
                    return self.four_oh_four("invalid tourney date %s" % ( parsed_date ))

                #validate the tourney type
                if not tourney_type in Tournaments.tourney_types:
                    return self.four_oh_four("invalid tourney type %s" % ( tourney_type ))

                #good to go!
                pm = PersistenceManager(myapp.db_connector)
                tourney = Tourney(tourney_name=tourney_name, tourney_date=tourney_date,
                            tourney_type=tourney_type, round_length=round_length, entry_date=parsed_date,
                            participant_count=participant_count, locked=False)
                pm.db_connector.get_session().add(tourney)

                #add email if it exists
                if t.has_key(EMAIL):
                    email = t[EMAIL]
                    #don't bother validating it :-)
                    tourney.email = email

                #venue gook
                if t.has_key(VENUE):
                    vhref = t[VENUE]
                    venue = TourneyVenue()
                    if vhref.has_key(COUNTRY):
                        venue.country = vhref[COUNTRY]
                    if vhref.has_key(STATE):
                        venue.state = vhref[STATE]
                    if vhref.has_key(CITY):
                        venue.city = vhref[CITY]
                    if vhref.has_key(VENUE):
                        venue.venue = vhref[VENUE]
                    tourney.venue = venue

                #now see if the players are there.  if so, add 'em
                if t.has_key(PLAYERS):
                    players = t[PLAYERS]
                    i = 1
                    for p in players:
                        player  = TourneyPlayer( player_name="Player %d" % ( i ) )
                        ranking = TourneyRanking( player=player)
                        tourney_list = TourneyList( tourney=tourney, player=player )
                        tourney.tourney_players.append( player )
                        tourney.tourney_lists.append( tourney_list )

                        i = i + 1
                        if p.has_key( PLAYER_NAME ):
                            player.player_name = p[PLAYER_NAME]
                        if p.has_key( MOV ):
                            ranking.mov = p[ MOV ]
                        if p.has_key( SCORE ):
                            ranking.score = p[SCORE]
                        if p.has_key( SOS ):
                            ranking.sos = p[SOS]
                        if p.has_key(DROPPED):
                            ranking.dropped = p[DROPPED]
                        if p.has_key( RANK ):
                            r = p[RANK]
                            if r.has_key( SWISS ):
                                ranking.swiss = r[SWISS]
                            if r.has_key( ELIMINATION ):
                                ranking.elim_rank  = r[ELIMINATION]

                pm.db_connector.get_session().commit()

                response=jsonify( { TOURNAMENT : { NAME : tourney.tourney_name, "id": tourney.id}})
                response.status_code = 201
                return response

            else:
                return self.four_oh_four("invalid tourney submission, must contain required fields, missing %s " % ( TOURNAMENTS ) )
        else:
            return self.four_oh_four("invalid tourney submission, must contain a json payload" )


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


