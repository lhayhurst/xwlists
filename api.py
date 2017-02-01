from decoder import decode

__author__ = 'lhayhurst'

import uuid
import json

from flask import jsonify, request, abort
from flask.ext import restful
import dateutil.parser
from sqlalchemy import func, or_

from xwingmetadata import sets_and_expansions
import myapp
from persistence import PersistenceManager, Tourney, TourneyVenue, TourneyPlayer, TourneyRanking, TourneyList, \
    RoundResult, TourneyRound, RoundType, TourneySet, Event
from xws import XWSToJuggler, XWSListConverter

PLAYER_ID = 'player_id'
PLAYER2_ID = 'player2_id'
PLAYER1_ID = 'player1_id'
PLAYERS = 'players'
PLAYER = 'player'
NEW_PLAYER_NAME = 'new_name'
BYE = 'bye'
DRAW = 'draw'
WIN = 'win'
FORMAT = 'format'

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
LIST = 'list'
TOURNAMENTS = "tournaments"
LEAGUES = 'leagues'
CITY = 'city'
STATE = 'state'
COUNTRY = 'country'
VENUE = 'venue'
EMAIL = 'email'
XWS = 'list'
FINAL_SALVO = 'final_salvo'
WINNER = 'winner'


class TournamentApiHelper:
    required_fields = [NAME, DATE, TYPE, ROUND_LENGTH, PARTICIPANT_COUNT]
    tourney_types = ["World Championship", "Nationals", "Regional", "Store Championship", "Vassal play", "Other"]
    valid_sets = sets_and_expansions.keys()

    def __init__(self,pm):
        self.pm = pm

    def check_token(self, json_data, tourney):
        if not json_data.has_key(API_TOKEN):
            return self.bail("Missing API token json, bailing out ...", 403)
        api_token = json_data[API_TOKEN]
        if not api_token == tourney.api_token:
            return self.bail("Token_id did not match, bailing out ....", 403)
        return None


    def convert_round_type_string(self, str):
        if str == SWISS:
            return RoundType.PRE_ELIMINATION
        if str == ELIMINATION:
            return RoundType.ELIMINATION
        return ""

    def missing_required_field(self, t):
        for rf in TournamentApiHelper.required_fields:
            if not t.has_key(rf):
                return rf
        return None

    def isint(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def bail(self, text, code):
        response = jsonify(message=text)
        response.status_code = code
        return response

    def extract_email(self, t, tourney):
        # add email if it exists
        if t.has_key(EMAIL):
            email = t[EMAIL]
            # don't bother validating it :-)
            tourney.email = email

    def extract_tourney_format(self, t, tourney):
        if t.has_key(FORMAT):
            tourney.format = t[FORMAT]

    def extract_venue(self, t, tourney):
        if t.has_key(VENUE):
            vhref = t[VENUE]
            country = None
            state   = None
            city    = None
            venue   = None

            if vhref.has_key(COUNTRY):
                country = vhref[COUNTRY]
            if vhref.has_key(STATE):
                state = vhref[STATE]
            if vhref.has_key(CITY):
                city = vhref[CITY]
            if vhref.has_key(VENUE):
                venue = vhref[VENUE]

            venue = self.pm.get_tourney_venue(country,state,city,venue)
            tourney.venue = venue

    def extract_player(self, p, player, ranking):
        if p.has_key(PLAYER_NAME):
            player.player_name = p[PLAYER_NAME]
        if p.has_key(MOV):
            ranking.mov = p[MOV]
        if p.has_key(SCORE):
            ranking.score = p[SCORE]
        if p.has_key(SOS):
            ranking.sos = float(p[SOS])
        if p.has_key(DROPPED):
            ranking.dropped = p[DROPPED]
        if p.has_key(RANK):
            r = p[RANK]
            if r.has_key(SWISS):
                ranking.rank = r[SWISS]
            if r.has_key(ELIMINATION):
                ranking.elim_rank = r[ELIMINATION]

    def extract_players(self, t, tourney):
        pm = PersistenceManager(myapp.db_connector)
        tlists_by_id = {}
        tlists_by_name = {}

        if t.has_key(PLAYERS):
            players = t[PLAYERS]
            i = 1
            for p in players:
                player = None
                ranking = None

                # first see if the tourney already has a player and player list matching this player's name
                #if so, update it rather than creating a new one
                if p.has_key(PLAYER_ID):
                    player = tourney.get_player_by_id(p[PLAYER_ID])
                    if player is None:
                        return self.bail(
                            "couldn't find player with id %d, giving up" % ( p[PLAYER_ID], 403)), None, None
                else:
                    if not p.has_key(PLAYER_NAME):
                        return self.bail("neither an id or a name was provided, giving up ", 403), None, None
                    player = tourney.get_player_by_name(p[PLAYER_NAME])

                if player is None:
                    player = TourneyPlayer(player_name="Player %d" % ( i ))
                    ranking = TourneyRanking(player=player)
                    player.result = ranking
                    tourney_list = TourneyList(tourney=tourney, player=player)
                    tlists_by_id[player.id] = tourney_list  # stash it away for later use
                    if p.has_key(PLAYER_NAME):
                        tlists_by_name[p[PLAYER_NAME]] = tourney_list
                    tourney.tourney_players.append(player)
                    tourney.tourney_lists.append(tourney_list)
                    tourney.rankings.append(ranking)
                    player.tourney_lists.append(tourney_list)
                    i = i + 1
                else:
                    ranking = player.result
                    tlists_by_id[player.id] = player.get_first_tourney_list()
                    if p.has_key(PLAYER_NAME):
                        tlists_by_name[p[PLAYER_NAME]] = tlists_by_id[player.id]

                # add list via XWS
                if XWS in p:
                    try:
                        XWSToJuggler(p[XWS]).convert(pm, tourney_list)
                    except Exception as e:
                        print "Could not convert XWS: {} (XWS was {!r})".format(e, p[XWS])

                self.extract_player(p, player, ranking)

        return None, tlists_by_id, tlists_by_name

    def extract_set(self, t, tourney, pm):
        if t.has_key(SETS_USED):
            sets_used = t[SETS_USED]
            for s in sets_used:
                if not s in TournamentApiHelper.valid_sets:
                    return self.helper.bail("unknown xwing set %s provided, bailing out" % ( s ), 403)
                set = pm.get_set(s)
                if set is None:
                    return self.helper.bail("unknown xwing set %s provided, bailing out" % ( s ), 403)
                ts = TourneySet(tourney=tourney, set=set)
                pm.db_connector.get_session().add(ts)
            return None
        return None


    def extract_rounds(self, tournament_json, tourney, tlists_by_id, tlists_by_name, pm):
        if not tournament_json.has_key(ROUNDS):
            return None

        for r in tournament_json[ROUNDS]:
            if not r.has_key(ROUND_TYPE):
                return self.helper.bail("Round type not found in tourney rounds, giving up!", 403)
            round_type = self.convert_round_type_string(r[ROUND_TYPE])
            if round_type is None:
                return self.helper.bail("Round type %s is not valid, giving up!" % ( round_type ), 403)
            if not r.has_key(ROUND_NUMBER):
                return self.helper.bail("Round number not found in tourney rounds, giving up!", 403)
            if not r.has_key(MATCHES):
                return self.helper.bail("List of match results not found in tourney round, giving up!", 403)


        # if any rounds exist, just take them all out and start from scratch
        if len(tourney.rounds) > 0:
            tourney.reset_rounds(pm.db_connector.get_session())

        for r in tournament_json[ROUNDS]:
            round_number = r[ROUND_NUMBER]
            round_type = self.convert_round_type_string(r[ROUND_TYPE])
            tourney_round = TourneyRound(round_num=round_number, round_type=round_type, tourney=tourney)
            tourney.rounds.append(tourney_round)
            pm.db_connector.get_session().add(tourney_round)

            matches = r[MATCHES]

            for m in matches:
                player1_name = None
                player1_id = None
                if m.has_key(PLAYER1):
                    player1_name = m[PLAYER1]
                if m.has_key(PLAYER1_ID):
                    player1_id = m[PLAYER1_ID]
                if player1_name is None and player1_id is None:
                    return self.helper.bail("Player one name and id not found in match, giving up!", 403)

                #get the list
                player1_list = None
                if player1_name is not None and tlists_by_name.has_key(player1_name):
                    player1_list = tlists_by_name[player1_name]
                elif player1_id is not None and tlists_by_id.has_key(player1_id):
                    player1_list = tlists_by_id[player1_id]
                if player1_list is None:
                    return self.helper.bail("PlayerOne's list could not be found, giving up ", 403)

                if not m.has_key(RESULT):
                    return self.helper.bail("Result not found in match, giving up!", 403)
                result = m[RESULT]
                round_result = None

                if result == WIN or result == DRAW:
                    player2_name = None
                    player2_id = None
                    if m.has_key(PLAYER2):
                        player2_name = m[PLAYER2]
                    if m.has_key(PLAYER2_ID):
                        player2_id = m[PLAYER2_ID]
                    if player2_name is None and player2_id is None:
                        return self.helper.bail("Player two name and id not found in match, giving up!", 403)

                    #get the list
                    player2_list = None
                    if player2_name is not None and tlists_by_name.has_key(player2_name):
                        player2_list = tlists_by_name[player2_name]
                    elif player2_id is not None and tlists_by_id.has_key(player2_id):
                        player2_list = tlists_by_id[player2_id]
                    if player2_list is None:
                        return self.helper.bail("Player2's list could not be found, giving up ", 403)

                    if not m.has_key(PLAYER1_POINTS):
                        return self.helper.bail("Player one points not found in match, giving up!", 403)
                    player1_points = m[PLAYER1_POINTS]
                    if not m.has_key(PLAYER2_POINTS):
                        return self.helper.bail("Player two points not found in match, giving up!", 403)
                    player2_points = m[PLAYER2_POINTS]
                    was_draw = False
                    if result == DRAW:
                        was_draw = True
                    winner = None
                    loser = None

                    if player1_points > player2_points:
                        winner = player1_list
                        loser = player2_list
                    elif player2_points > player1_points:
                        winner = player2_list
                        loser = player1_list

                    final_salvo = False
                    if m.has_key(FINAL_SALVO):
                        final_salvo = m[FINAL_SALVO]
                        if not m.has_key(WINNER):
                            return self.helper.bail("No winner provided for final salvo result", 403)
                        winner_name = m[WINNER]
                        if winner_name == player1_name:
                            winner = player1_list
                            loser  = player2_list
                        elif winner_name == player2_name:
                            winner = player2_list
                            loser  = player1_list
                        else:
                            return self.helper.bail("unknown player %s provided as winner" % ( winner_name ) )

                    #create a new result unless it already exists
                    round_result = RoundResult(round=tourney_round, list1=player1_list,
                                               list2=player2_list,
                                               winner=winner, loser=loser,
                                               list1_score=player1_points,
                                               list2_score=player2_points,
                                               bye=False,
                                               draw=was_draw,
                                               final_salvo = final_salvo)

                    tourney_round.results.append(round_result)

                elif result == BYE:
                    round_result = RoundResult(round=tourney_round, list1=player1_list,
                                               list2=None, winner=None, loser=None,
                                               list1_score=None,
                                               list2_score=None, bye=True, draw=False)
                    tourney_round.results.append(round_result)
                else:
                    return self.helper.bail("Unknown match result %s, giving up!" % ( result ), 403)
                tourney_round.results.append(round_result)
                pm.db_connector.get_session().add(round_result)

        pm.db_connector.get_session().flush()
        return None


class VassalLeaguesAPI(restful.Resource):
    def get(self):
        pm = PersistenceManager(myapp.db_connector)
        leagues = pm.get_leagues()
        ret = []
        for l in leagues:
            ret.append(l.id)
        return json.dumps({LEAGUES: ret})

LEAGUE_NAME = 'name'
LEAGUE_CHALLONGE_NAME = 'challonge_name'
LEAGUE_TIERS = 'tiers'
TIER_NAME = 'name'
TIER_CHALLONGE_NAME = 'challonge_name'
TIER_PLAYERS = 'players'
TIER_DIVISIONS = 'divisions'
TIER_ID = 'tier_id'
PLAYER_NAME = 'name'
PLAYER_ID = 'player_id'
DIVISION_NAME = 'name'
DIVISION_CHALLONGE_NAME = 'challonge_name'
DIVISION_ID = 'division_id'
DIVISION_PLAYERS = 'players'


class VassalLeagueAPI(restful.Resource):
    def get(self,league_id):
        pm = PersistenceManager(myapp.db_connector)
        league = pm.get_league_by_id(league_id)
        ret = {}
        ret[LEAGUE_NAME] = league.name
        ret[LEAGUE_CHALLONGE_NAME] = league.challonge_name
        tiers = league.tiers
        tiers_data = []
        ret[LEAGUE_TIERS] = tiers_data

        for t in tiers:
            tdata = {
                TIER_NAME : t.name,
                TIER_CHALLONGE_NAME : t.challonge_name,
                TIER_DIVISIONS : [],
                TIER_ID : t.id
            }

            for division in t.divisions:
                division_players = []
                for player in division.players:
                    division_players.append( { PLAYER_NAME : player.name, PLAYER_ID: player.id} )
                tdata[TIER_DIVISIONS].append( { DIVISION_NAME : division.name,
                                                DIVISION_CHALLONGE_NAME : division.challonge_name,
                                                DIVISION_ID: division.id,
                                                DIVISION_PLAYERS : division_players
                                                })

            tiers_data.append(tdata)
        return json.dumps(ret)

DIVISION_RANKING = 'division_ranking'
TIER_RANKING     = 'tier_ranking'
class VassalLeagueRanking(restful.Resource):
    def get(self, league_id, tier_id):
        pm = PersistenceManager(myapp.db_connector)
        tier = pm.get_tier_by_id(tier_id)
        ret = {}
        if tier is None:
            return json.dumps(ret)

        division_rankings = []
        tier_rankings     = []
        ret[ DIVISION_RANKING] = division_rankings
        ret[ TIER_RANKING ] = tier_rankings

        for d in tier.divisions:
            dr = { 'division_name' : d.name,
                   'division_challonge_name' : d.challonge_name,
                   'division_id' : d.id,
                   'rankings' : []
                   }
            division_rankings.append(dr)
            for r in d.get_ranking(ignore_defaults=False):
                dr['rankings'].append(
                    {
                        'rank'  : r['rank'],
                        'wins'  : r['wins'],
                        'loses' : r['losses'],
                        'draws' : r['draws'],
                        'mov'   : r['mov'],
                        'id'    : r['player'].id,
                        'name'  : r['player'].name,
                    })

        for r in tier.get_ranking(ignore_defaults=False):
            tier_rankings.append( {
                        'rank'  : r['rank'],
                        'wins'  : r['wins'],
                        'losses' : r['losses'],
                        'draws' : r['draws'],
                        'mov'   : r['mov'],
                        'id'    : r['player'].id,
                        'name'  : r['player'].name,
                    })

        return json.dumps(ret)

class TournamentsAPI(restful.Resource):
    def get(self):
        pm = PersistenceManager(myapp.db_connector)
        ids = pm.get_tourney_ids()
        ret = []
        for id in ids:
            ret.append(id[0])
        return json.dumps({TOURNAMENTS: ret})


    def post(self):
        json_data = None
        pm = PersistenceManager(myapp.db_connector)

        helper = TournamentApiHelper(pm)
        self.helper = helper

        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)
        if json_data is not None:
            if json_data.has_key(TOURNAMENT):
                t = json_data[TOURNAMENT]

                # it should have all the required fields
                missing_field = helper.missing_required_field(t)
                if missing_field is not None:
                    return helper.bail(
                        "invalid tourney submission, must contain required fields, missing %s " % ( missing_field ),
                        403)

                tourney_name = t[NAME]
                tourney_date = t[DATE]
                tourney_type = t[TYPE]
                round_length = t[ROUND_LENGTH]
                participant_count = t[PARTICIPANT_COUNT]

                # validate the tourney date
                parsed_date = None
                try:
                    parsed_date = dateutil.parser.parse(tourney_date)
                except Exception:
                    return helper.bail("invalid tourney date %s" % ( parsed_date ), 403)

                #validate the tourney type
                if not tourney_type in TournamentApiHelper.tourney_types:
                    return helper.bail("invalid tourney type %s" % ( tourney_type ), 403)

                #good to go!
                tourney = Tourney(tourney_name=tourney_name, tourney_date=tourney_date,
                                  tourney_type=tourney_type, round_length=round_length, entry_date=parsed_date,
                                  participant_count=participant_count, locked=False)
                pm.db_connector.get_session().add(tourney)

                helper.extract_email(t, tourney)
                helper.extract_tourney_format(t, tourney)
                helper.extract_venue(t, tourney)
                #now see if the players are there.  if so, add 'em
                bail, tlists_by_id, tlists_by_name = helper.extract_players(t,
                                                                            tourney)  #round by round results, if it exists

                if bail:
                    return bail

                #set gook
                bailout = helper.extract_set(t, tourney, pm)
                if bailout:
                    return bailout

                bailout = helper.extract_rounds(t, tourney, tlists_by_id, tlists_by_name, pm)
                if bailout:
                    return bailout

                #looking good.
                #grab a uuid to finish the job
                tourney.api_token = str(uuid.uuid4())

                #and log it
                event = Event(remote_address=myapp.remote_address(request),
                              event_date=func.now(),
                              event="API",
                              event_details="tournament API: tourney creation via POST")

                pm.db_connector.get_session().add(event)
                pm.db_connector.get_session().commit()

                players = []
                for player in tourney.tourney_players:
                    players.append({NAME: player.get_player_name(), ID: player.id})

                response = jsonify({TOURNAMENT: {NAME: decode(tourney.tourney_name),
                                                 ID: tourney.id,
                                                 API_TOKEN: tourney.api_token,
                                                 PLAYERS: players}})
                response.status_code = 201
                return response

            else:
                return helper.bail(
                    "invalid tourney submission, must contain required fields, missing %s " % ( TOURNAMENTS ), 403)
        else:
            return helper.bail("invalid tourney submission, must contain a json payload", 403)


class PlayerAPI(restful.Resource):
    def delete(self, tourney_id, player_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)

        if not helper.isint(tourney_id):
            return helper.bail("invalid tourney_id  %d passed to player delete" % ( tourney_id), 403)
        if not helper.isint(player_id):
            return helper.bail("invalid player  %d passed to player delete" % ( player_id), 403)
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        bail = helper.check_token(json_data, tourney)
        if bail:
            return bail
        player = tourney.get_player_by_id(player_id)
        if player is None:
            return helper.bail("couldn't find player %d, bailing out" % ( player_id), 403)
        pm.db_connector.get_session().delete(player)
        pm.db_connector.get_session().commit()

    def post(self, tourney_id, player_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)

        if not helper.isint(tourney_id):
            return helper.bail("invalid tourney_id  %d passed to player post" % ( tourney_id), 400)
        if not helper.isint(player_id):
            return helper.bail("invalid player  %d passed to player post" % ( player_id), 400)
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        bail = helper.check_token(json_data, tourney)
        if bail:
            return bail
        player = tourney.get_player_by_id(player_id)
        if player is None:
            return helper.bail("couldn't find player %d, bailing out" % ( player_id), 400)

        dirty = False

        # add list via XWS
        if XWS in json_data:
            dirty = True
            try:
                tourney_list = player.tourney_lists[-1]
                XWSToJuggler(json_data[XWS]).convert(pm, tourney_list)
            except:
                pm.db_connector.get_session().rollback()
                return helper.bail('Could not add list via XWS', 400)

        # other potential edits

        if dirty:
            pm.db_connector.get_session().commit()

        return jsonify({
            'player': {
                'id': player.id,
                'tourney_id': tourney.id,
                'name': player.get_player_name(),
            }
        })


class PlayersAPI(restful.Resource):
    def get(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        if not helper.isint(tourney_id):
            return helper.bail("invalid tourney_id  %d passed to player get" % ( tourney_id), 403)
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        if tourney is None:
            return helper.bail("failed to look up tourney id %d for player get" % ( tourney_id), 403)

        players = []
        for player in tourney.tourney_players:
            players.append({NAME: player.get_player_name(), ID: player.id})

        response = jsonify({PLAYERS: players})
        response.status_code = 200
        return response

    def put_or_post(self, helper, tourney_id):
        if not helper.isint(tourney_id):
            return helper.bail("invalid tourney_id  %d passed to player get" % ( tourney_id), 403)
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        if tourney is None:
            return helper.bail("failed to look up tourney id %d for player get" % ( tourney_id), 403)

        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)
        if json_data is not None:
            bail = helper.check_token(json_data, tourney)
            if bail:
                return bail, None
        if not json_data.has_key(PLAYERS):
            return helper.bail("player put missing player key", 403), None

        bail, tl1, tl2 = helper.extract_players(json_data, tourney)
        if bail:
            return bail
        pm.db_connector.get_session().commit()

        players = []
        for player in tourney.tourney_players:
            players.append({NAME: player.get_player_name(), ID: player.id})
        return None, players

    def post(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        bail, players = self.put_or_post(helper, tourney_id)
        if bail:
            return bail
        # only return the players that the caller created
        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)
        new_players = json_data[PLAYERS]
        ret = []
        for p in players:
            for np in new_players:
                if p[NAME] == np[PLAYER_NAME]:
                    ret.append(p)

        response = jsonify({PLAYERS: ret})
        response.status_code = 201
        return response

    def put(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        bail, players = self.put_or_post(helper, tourney_id)
        if bail:
            return bail


class TourneyToJsonConverter:
    def convert(self, t):
        tournament = {}
        ret = {}
        ret[TOURNAMENT] = tournament
        tournament[ID] = t.id
        tournament[NAME] = t.get_tourney_name()
        tournament[DATE] = str(t.tourney_date)
        tournament[TYPE] = t.tourney_type
        tournament[ROUND_LENGTH] = t.round_length
        if t.format is not None:
            tournament[FORMAT] = t.format

        # build the tournament to ranking map
        # naive assumption: assume the rankings are there
        players = []
        tournament[PLAYERS] = players
        for ranking in t.rankings:
            player = {}
            player[PLAYER_NAME] = ranking.player.get_player_name()
            player[SCORE] = ranking.score
            player[MOV] = ranking.mov
            sos = "%.2f" % ranking.sos
            player[SOS] = sos
            rank = {}
            player[RANK] = rank
            rank[SWISS] = ranking.rank
            if ranking.elim_rank is not None:
                rank[ELIMINATION] = ranking.elim_rank
            players.append(player)

            #if the player has a list, xws it
            tlist = ranking.player.get_first_tourney_list()
            if tlist:
                converter = XWSListConverter(tlist)
                player[LIST] = converter.data

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
                if result.final_salvo is not None:
                    resref[FINAL_SALVO] = result.final_salvo

        return ret


class TournamentAPI(restful.Resource):
    def put(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        if tourney is None:
            response = jsonify(message="tourney %d not found" % ( tourney_id ))
            response.status_code = 403
            return response

        # go through and try to update what we can.
        json_data = None
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        self.helper = helper

        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)
        if json_data is not None:

            bail = helper.check_token(json_data, tourney)
            if bail:
                bail

            if json_data.has_key(TOURNAMENT):
                t = json_data[TOURNAMENT]
                if t.has_key(NAME):
                    tourney.tourney_name = t[NAME]
                if t.has_key(DATE):
                    tourney_date = t[DATE]
                    parsed_date = None
                    try:
                        parsed_date = dateutil.parser.parse(tourney_date)
                    except Exception:
                        return helper.bail("invalid tourney date %s" % ( parsed_date ), 403)
                    tourney.tourney_date = parsed_date
                if t.has_key(TYPE):
                    tourney_type = t[TYPE]
                    #validate the tourney type
                    if not tourney_type in TournamentApiHelper.tourney_types:
                        return helper.bail("invalid tourney type %s" % ( tourney_type ), 403)
                    tourney.tourney_type = tourney_type

                if t.has_key(ROUND_LENGTH):
                    tourney.round_length = t[ROUND_LENGTH]

                if t.has_key(PARTICIPANT_COUNT):
                    tourney.participant_count = t[PARTICIPANT_COUNT]

                #now try all the other fields.
                helper.extract_email(t, tourney)
                helper.extract_tourney_format(t, tourney)
                helper.extract_venue(t, tourney)
                bail, tlists_by_id, tlists_by_name = helper.extract_players(t,
                                                                            tourney)  #round by round results, if it exists
                if bail:
                    return bail
                bailout = helper.extract_set(t, tourney, pm)
                if bailout:
                    return bailout

                bailout = helper.extract_rounds(t, tourney, tlists_by_id, tlists_by_name, pm)
                if bailout:
                    return bailout

                #and log it
                event = Event(remote_address=myapp.remote_address(request),
                              event_date=func.now(),
                              event="API",
                              event_details="tournament API: tourney update via POST")

                pm.db_connector.get_session().add(event)
                pm.db_connector.get_session().commit()

                response = jsonify(
                    {TOURNAMENT: {NAME: tourney.get_tourney_name(), "id": tourney.id, API_TOKEN: tourney.api_token}})
                response.status_code = 200
                return response

            else:
                return helper.bail(
                    "invalid tourney submission, must contain required fields, missing %s " % ( TOURNAMENTS ), 403)
        else:
            return helper.bail("invalid tourney submission, must contain a json payload", 403)


    def get(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        t = pm.get_tourney_by_id(tourney_id)
        if t is None:
            response = jsonify(message="tourney %d not found" % ( tourney_id ))
            response.status_code = 404
            return response

        # and log it
        event = Event(remote_address=myapp.remote_address(request),
                      event_date=func.now(),
                      event="API",
                      event_details="tournament API: tourney GET")
        pm.db_connector.get_session().add(event)

        pm.db_connector.get_session().commit()

        return jsonify(TourneyToJsonConverter().convert(t))

    def delete(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)
        self.helper = helper
        t = pm.get_tourney_by_id(tourney_id)
        if t is None:
            return helper.bail("tourney %d not found" % ( tourney_id ), 403)

        json_data = None
        try:
            json_data = request.get_json(force=True)
        except Exception:
            return helper.bail("bad json received!", 403)
        if json_data is None:
            return helper.bail("delete call for tourney_id %d missing json payload, giving up " % (tourney_id), 403)

        bail = helper.check_token(json_data, t)
        if bail:
            return bail

        # whew. aaaaalmost there...
        try:
            pm.delete_tourney_by_id(tourney_id)
        except Exception:
            return helper.bail("unable to delete tourney %d, bailing out " % ( tourney_id ), 403)

            #and log it
        event = Event(remote_address=myapp.remote_address(request),
                      event_date=func.now(),
                      event="API",
                      event_details="tournament API: tourney delete %d" % ( tourney_id ))
        pm.db_connector.get_session().add(event)
        pm.db_connector.get_session().commit()

        response = jsonify(message="deleted tourney id %d" % ( tourney_id ))
        response.status_code = 204
        return response


class TournamentSearchAPI(restful.Resource):
    '''
        Accepts POST { "query": "some_search_string" }
        Returns dict of tourney_id: tourney_data for substring query
        Substring is checked in tourney name and venue.
    '''

    def post(self):
        try:
            query = request.form['query']
        except KeyError:
            json_data = request.get_json(force=True)
            query = json_data['query']

        try:
            query = query.decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            abort(400)

        pm = PersistenceManager(myapp.db_connector)
        tourneys = pm.db_connector.get_session().query(Tourney) \
            .join(TourneyVenue) \
            .filter(
            or_(
                Tourney.tourney_name.like('%{}%'.format(query)),
                TourneyVenue.venue.like('%{}%'.format(query))
            )
        )

        response = {
            t.id: {
                'name': t.tourney_name,
                'venue': t.venue.venue,
                'date': t.tourney_date.strftime('%Y-%m-%d'),  # no timezone was kept :(
            }
            for t in tourneys}

        return jsonify(response)


class TournamentTokenAPI(restful.Resource):
    '''
        Accepts POST { "email": "email@used.to.create" }
        If email is valid, returns dict of api_token: api_token
        Creates api_token if needed.
    '''

    def post(self, tourney_id):
        pm = PersistenceManager(myapp.db_connector)
        helper = TournamentApiHelper(pm)

        try:
            email = request.form['email']
        except KeyError:
            json_data = request.get_json(force=True)
            email = json_data['email']

        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        if tourney is None:
            return helper.bail("tourney %d not found" % ( tourney_id ), 404)

        if email != tourney.email:
            return helper.bail("incorrect email for tourney {}".format(tourney_id), 404)

        if tourney.api_token is None:
            tourney.api_token = str(uuid.uuid4())
            pm.db_connector.get_session().commit()

        return jsonify({"api_token": tourney.api_token})
