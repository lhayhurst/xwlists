

FORMAT = 'format'
__author__ = 'lhayhurst'

import uuid
from xwingmetadata import sets_and_expansions
import json
from flask import jsonify, request
import myapp
from persistence import PersistenceManager, Tourney, TourneyVenue, TourneyPlayer, TourneyRanking, TourneyList, \
    RoundResult, TourneyRound, RoundType, TourneySet, Event
from flask.ext import restful
import dateutil.parser
from sqlalchemy import func

API_TOKEN = "api_token"
SETS_USED = 'sets_used'
DROPPED = 'dropped'
VENUE = 'venue'
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
        return json.dumps({TOURNAMENTS: ret})

    required_fields = [NAME, DATE, TYPE, ROUND_LENGTH, PARTICIPANT_COUNT]
    tourney_types = ["World Championship", "Nationals", "Regional", "Store Championship", "Vassal play", "Other"]
    valid_sets = sets_and_expansions.keys()

    def convert_round_type_string(self, str):
        if str == SWISS:
            return RoundType.PRE_ELIMINATION
        if str == ELIMINATION:
            return RoundType.ELIMINATION
        return ""

    def missing_required_field(self, t):
        for rf in Tournaments.required_fields:
            if not t.has_key(rf):
                return rf
        return None

    def four_oh_four(self, text):
        response = jsonify(message=text)
        response.status_code = 404
        return response

    def post(self):
        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return self.four_oh_four("bad json received!")
        if json_data is not None:
            if json_data.has_key(TOURNAMENT):
                t = json_data[TOURNAMENT]

                # it should have all the required fields
                missing_field = self.missing_required_field(t)
                if missing_field is not None:
                    return self.four_oh_four(
                        "invalid tourney submission, must contain required fields, missing %s " % ( missing_field ))

                tourney_name = t[NAME]
                tourney_date = t[DATE]
                tourney_type = t[TYPE]
                round_length = t[ROUND_LENGTH]
                participant_count = t[PARTICIPANT_COUNT]

                #validate the tourney date
                parsed_date = None
                try:
                    parsed_date = dateutil.parser.parse(tourney_date)
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

                if t.has_key(FORMAT):
                    tourney.format = t[FORMAT]

                #set gook
                if t.has_key(SETS_USED):
                    sets_used = t[SETS_USED]
                    for s in sets_used:
                        if not s in Tournaments.valid_sets:
                            return self.four_oh_four("unknown xwing set %s provided, bailing out" % ( s ))
                        set = pm.get_set(s)
                        if set is None:
                            return self.four_oh_four("unknown xwing set %s provided, bailing out" % ( s ))
                        ts = TourneySet(tourney=tourney, set=set)
                        pm.db_connector.get_session().add(ts)

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
                tlists = {}
                if t.has_key(PLAYERS):
                    players = t[PLAYERS]
                    i = 1
                    for p in players:
                        player = TourneyPlayer(player_name="Player %d" % ( i ))
                        ranking = TourneyRanking(player=player)
                        player.result = ranking
                        tourney_list = TourneyList(tourney=tourney, player=player)
                        tlists[player.player_name] = tourney_list  #stash it away for later use
                        tourney.tourney_players.append(player)
                        tourney.tourney_lists.append(tourney_list)
                        tourney.rankings.append(ranking)

                        i = i + 1
                        if p.has_key(PLAYER_NAME):
                            player.player_name = p[PLAYER_NAME]
                            tlists[player.player_name] = tourney_list
                        if p.has_key(MOV):
                            ranking.mov = p[MOV]
                        if p.has_key(SCORE):
                            ranking.score = p[SCORE]
                        if p.has_key(SOS):
                            ranking.sos = p[SOS]
                        if p.has_key(DROPPED):
                            ranking.dropped = p[DROPPED]
                        if p.has_key(RANK):
                            r = p[RANK]
                            if r.has_key(SWISS):
                                ranking.rank = r[SWISS]
                            if r.has_key(ELIMINATION):
                                ranking.elim_rank = r[ELIMINATION]

                #round by round results, if it exists
                if t.has_key(ROUNDS):
                    for r in t[ROUNDS]:
                        if not r.has_key(ROUND_TYPE):
                            return self.four_oh_four("Round type not found in tourney rounds, giving up!")
                        round_type = self.convert_round_type_string(r[ROUND_TYPE])
                        if round_type is None:
                            return self.four_oh_four("Round type %s is not valid, giving up!" % ( round_type ))
                        if not r.has_key(ROUND_NUMBER):
                            return self.four_oh_four("Round number not found in tourney rounds, giving up!")
                        round_number = r[ROUND_NUMBER]
                        if not r.has_key(MATCHES):
                            return self.four_oh_four("List of match results not found in tourney round, giving up!")
                        tourney_round = TourneyRound(round_num=round_number, round_type=round_type, tourney=tourney)
                        tourney.rounds.append(tourney_round)

                        matches = r[MATCHES]
                        for m in matches:
                            if not m.has_key(PLAYER1):
                                return self.four_oh_four("Player one not found in match, giving up!")
                            player1 = m[PLAYER1]
                            if not m.has_key(RESULT):
                                return self.four_oh_four("Result not found in match, giving up!")
                            if not tlists.has_key(player1):
                                return self.four_oh_four("Player %s 's list could not be found, giving up " % player1)

                            result = m[RESULT]
                            round_result = None
                            if result == 'win' or result == 'draw':
                                if not m.has_key(PLAYER2):
                                    return self.four_oh_four("Player two not found in match, giving up!")
                                player2 = m[PLAYER2]
                                if not tlists.has_key(player2):
                                    return self.four_oh_four(
                                        "Player %s 's list could not be found, giving up " % player2)

                                if not m.has_key(PLAYER1_POINTS):
                                    return self.four_oh_four("Player one points not found in match, giving up!")
                                player1_points = m[PLAYER1_POINTS]
                                if not m.has_key(PLAYER2_POINTS):
                                    return self.four_oh_four("Player two points not found in match, giving up!")
                                player2_points = m[PLAYER2_POINTS]
                                was_draw = False
                                if result == 'draw':
                                    was_draw = True
                                winner = None
                                loser = None

                                if player1_points > player2_points:
                                    winner = tlists[player1]
                                    loser = tlists[player2]
                                else:
                                    winner = tlists[player2]
                                    loser = tlists[player1]
                                round_result = RoundResult(round=tourney_round, list1=tlists[player1],
                                                           list2=tlists[player2],
                                                           winner=winner, loser=loser,
                                                           list1_score=player1_points,
                                                           list2_score=player2_points,
                                                           bye=False, draw=was_draw)
                            elif result == 'bye':
                                round_result = RoundResult(round=tourney_round, list1=tlists[player1],
                                                           list2=None, winner=None, loser=None,
                                                           list1_score=None,
                                                           list2_score=None, bye=True, draw=False)
                            else:
                                return self.four_oh_four("Unknown match result %s, giving up!" % ( result ))
                            tourney_round.results.append(round_result)

                #looking good.
                #grab a uuid to finish the job
                tourney.api_token = str(uuid.uuid4())

                #and log it
                event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="API",
                  event_details="tournament API: tourney creation via POST")

                pm.db_connector.get_session().add( event )

                pm.db_connector.get_session().commit()


                response = jsonify({TOURNAMENT: {NAME: tourney.tourney_name, "id": tourney.id, API_TOKEN: tourney.api_token }})
                response.status_code = 201
                return response

            else:
                return self.four_oh_four(
                    "invalid tourney submission, must contain required fields, missing %s " % ( TOURNAMENTS ))
        else:
            return self.four_oh_four("invalid tourney submission, must contain a json payload")


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
        if t.format is not None:
            tournament[FORMAT] = t.format

        # build the tournament to ranking map
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
            players.append(player)

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

    def four_oh_four(self, text):
        response = jsonify(message=text)
        response.status_code = 404
        return response

    def get(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        t = pm.get_tourney_by_id(tourney_id)
        if t is None:
            response = jsonify(message="tourney %d not found" % ( tourney_id ))
            response.status_code = 404
            return response

        #and log it
        event = Event(remote_address=myapp.remote_address(request),
          event_date=func.now(),
          event="API",
          event_details="tournament API: tourney GET")
        pm.db_connector.get_session().add( event )

        pm.db_connector.get_session().commit()

        return TourneyToJsonConverter().convert(t)

    def delete(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        t = pm.get_tourney_by_id(tourney_id)
        if t is None:
            return self.four_oh_four("tourney %d not found" % ( tourney_id ))

        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return self.four_oh_four("bad json received!")
        if json_data is None:
            return self.four_oh_four("delete call for tourney_id %d missing json payload, giving up " % (tourney_id))

        api_token = json_data[ API_TOKEN ]
        if not json_data.has_key(API_TOKEN):
            return self.four_oh_four("delete call is missing API token json, bailing out ...")

        if not api_token == t.api_token:
            return self.four_oh_four("delete call token_id did not match, bailing out ....")

        #whew. aaaaalmost there...
        try:
            pm.delete_tourney_by_id( tourney_id )
        except Exception:
            return self.four_oh_four("unable to delete tourney %d, bailing out " % ( tourney_id ) )

         #and log it
        event = Event(remote_address=myapp.remote_address(request),
          event_date=func.now(),
          event="API",
          event_details="tournament API: tourney delete %d" % ( tourney_id ))
        pm.db_connector.get_session().add( event )
        pm.db_connector.get_session().commit()


        response = jsonify(message="deleted tourney id %d" % ( tourney_id ))
        response.status_code = 204
        return response
