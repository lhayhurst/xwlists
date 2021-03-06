import json
import os
from random import randint
import urllib
import uuid
import sys
from datetime import datetime, timedelta

from datatables import ColumnDT, DataTables
from flask import render_template, request, url_for, redirect, jsonify, Response, flash, send_file, send_from_directory
from flask_mail import Mail, Message

from pytz import common_timezones, timezone

from uidgen import ListUIDGen
from xwvassal_league import CURRENT_VASSAL_LEAGUE_NAME, XWingVassalLeagueHelper

reload(sys)
sys.setdefaultencoding("utf-8")
import re
from geopy import Nominatim
from markupsafe import Markup
import sqlalchemy

from sqlalchemy import func
from sqlalchemy import Date
from werkzeug.utils import secure_filename
from requests import post
from api import TournamentsAPI, TournamentAPI, TournamentAPIWithPoints, PlayersAPI, PlayerAPI, TournamentSearchAPI, TournamentTokenAPI, \
    VassalLeaguesAPI, VassalLeagueAPI, \
    VassalLeagueRanking, VassalLeagueMatches


from cryodex import Cryodex
from dataeditor import RankingEditor, RoundResultsEditor
from decoder import decode
import myapp
from persistence import Tourney, TourneyList, PersistenceManager, Faction, Ship, ShipUpgrade, TourneyRound, RoundResult, \
    TourneyPlayer, TourneyRanking, TourneySet, \
    Event, ArchtypeList, LeagueMatch, \
    TierPlayer, EscrowSubscription, League, Tier, Division, TourneyVenue
from rollup import ShipPilotTimeSeriesData, ShipTotalHighchartOptions, FactionTotalHighChartOptions, \
    ShipHighchartOptions, PilotHighchartOptions, UpgradeHighChartOptions, PilotSkillTimeSeriesData, \
    PilotSkillHighchartsGraph
from search import Search
import xwingmetadata
from xws import VoidStateXWSFetcher, XWSToJuggler, YASBFetcher, FabFetcher, GeneralXWSFetcher, XWSListConverter
import flask_restful as restful
#from flask.ext import restful
from flask_cors import CORS

YASB = 'yasb'

VOIDSTATE = "voidstate"

app = myapp.create_app()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
STATIC_ROOT = "static"
UPLOAD_FOLDER = "static/tourneys"
VLOG_FOLDER = "static/vlog"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'html', 'json', 'tsv', 'vlog'])

is_maintenance_mode = False

here = os.path.dirname(__file__)
static_dir = os.path.join(here, app.config['UPLOAD_FOLDER'])
static_root = os.path.join(here, STATIC_ROOT)
vlog_dir = os.path.join(here, VLOG_FOLDER)

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
DO_MAIL = os.environ.get('DO_MAIL')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

from werkzeug.contrib.cache import SimpleCache

simple_cache = SimpleCache()
xwing_data   = SimpleCache()

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD
))

# administrator list
ADMINS = [ADMIN_EMAIL]

mail = Mail(app)

session = myapp.db_connector.get_session()

api = restful.Api(app)
api.add_resource(VassalLeaguesAPI, '/api/v1/vassal_leagues')
api.add_resource(VassalLeagueAPI, '/api/v1/vassal_league/<int:league_id>')
api.add_resource(VassalLeagueRanking, '/api/v1/vassal_league_ranking/<int:league_id>/tier/<int:tier_id>/')
api.add_resource(VassalLeagueMatches, '/api/v1/vassal_league_matches/<int:league_id>')

api.add_resource(TournamentsAPI, '/api/v1/tournaments')
api.add_resource(TournamentAPI, '/api/v1/tournament/<int:tourney_id>')
api.add_resource(TournamentAPIWithPoints, '/api/v2/tournament/<int:tourney_id>')

api.add_resource(PlayersAPI, '/api/v1/tournament/<int:tourney_id>/players')
api.add_resource(PlayerAPI, '/api/v1/tournament/<int:tourney_id>/player/<int:player_id>')

api.add_resource(TournamentSearchAPI, '/api/v1/search/tournaments')
api.add_resource(TournamentTokenAPI, '/api/v1/tournament/<int:tourney_id>/token')


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def mail_message(subject, message):
    msg = Message(subject, sender=ADMINS[0], recipients=ADMINS)
    msg.body = 'text body'
    msg.html = '<b>A Message From XWJuggler</b><br><hr>' + message
    with app.app_context():
        if DO_MAIL:
            mail.send(msg)


def mail_error(errortext):
    msg = Message('XWJuggler Error', sender=ADMINS[0], recipients=ADMINS)
    msg.body = 'text body'
    msg.html = '<b>ERROR</b><br><hr>' + errortext
    with app.app_context():
        if DO_MAIL:
            mail.send(msg)


is_maintenance_mode = False


@app.before_request
def check_for_maintenance():
    if is_maintenance_mode and request.path != url_for('maintenance'):
        return redirect(url_for('maintenance'))


@app.route('/robots.txt')
def static_from_root():
 return send_from_directory(app.static_folder, request.path[1:])

@app.route('/maintenance')
def maintenance():
    return 'List Juggler is down for some database maintenance, we should we back shortly, may the force be with you!', 503


@app.route('/')
def index():
    return redirect("/tourneys")


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/fix_archtype_keys")
def regenerate_archtype_keys():
    pm = PersistenceManager(myapp.db_connector)
    archtypes = pm.get_all_archtypes()
    i = 0
    for a in archtypes:
        hashkey = a.generate_hash_key(a.ships)
        a.hashkey = hashkey
        if i % 1000 == 0:
            print "hashed %d records " % (i)
        i = i + 1
    pm.db_connector.get_session().commit()


@app.route("/fix_archtype_dupes")
def fix_archtype_dupes():
    pm = PersistenceManager(myapp.db_connector)
    f = ListUIDGen(pm)
    f.fix_dupes()
    return redirect("/")

@app.route("/manage_escrows")
def manage_escrows():
    league_id = request.args.get('league_id')
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league_by_id(league_id)

    matches = []
    for tier in league.tiers:
        for match in tier.matches:
            matches.append(match)

    return render_template('manage_escrows.html', matches=matches)


@app.route("/set_up_escrow_subscription")
def set_up_escrow_subscription():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)

    # first delete all the old subscriptions
    pm.delete_all_subscriptions()
    pm.db_connector.get_session().commit()

    matches = []
    for tier in league.tiers:
        for player in tier.players:
            for match in player.matches:
                es = EscrowSubscription(observer=player, match=match)
                pm.db_connector.get_session().add(es)
                matches.append(match)
    pm.db_connector.get_session().commit()
    return render_template("escrow_subscriptions.html", matches=matches)


@app.route("/escrow_subscriptions")
def escrow_subscriptions():
    league_id = request.args.get('league_id')
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league_by_id(league_id)
    matches = []
    for tier in league.tiers:
        for player in tier.players:
            for match in player.matches:
                matches.append(match)
    return render_template("escrow_subscriptions.html", matches=matches)

@app.route("/fix_escrow_bs")
def fix_escrow_bs():
    return render_template("fix_escrow_bs.html")

@app.route("/fix_escrow_form_results", methods=['POST'])
def fix_escrow_form_results():
    escrow_json_file = request.files['escrow_file']
    raw_json = escrow_json_file.read()
    escrowed_lists = json.loads(raw_json)

    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)
    helper = XWingVassalLeagueHelper(name=league.name, number=league.id)
    helper.update_escrowed_lists(pm, league, escrowed_lists)
    return redirect("/league")


@app.route("/add_league")
def create_league():
    return render_template("add_league.html")


@app.route("/add_league_form_results", methods=['POST'])
def add_league_form_results():
    league_name = decode(request.form['name'])
    season_number = decode(request.form['season_number'])
    league_file = request.files['league_file']

    helper = XWingVassalLeagueHelper(league_name, season_number, league_file)
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(league_name)
    #if league is None:
    helper.create_league(pm,league)
    return redirect("/league")


@app.route("/create_league_matches")
def create_league_matches():
    league_id = request.args.get('league_id')
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league_by_id(league_id)
    helper = XWingVassalLeagueHelper(name=league.name, number=league.id)
    helper.create_matchups(pm, league)
    return redirect("/league")

@app.route("/league_player")
def league_player():
    player_id = request.args.get('player_id')
    pm = PersistenceManager(myapp.db_connector)
    player = pm.get_league_player_by_id(player_id)
    player_stats = player.get_stats(mercenary_mode=True) #for player home page, all matches are shown
    return render_template("league_player.html", player=player, stats=player_stats)


@app.route("/tier_rankings")
def tier_rankings():
    tier_id = request.args.get('tier_id')
    ignore_defaults = request.args.get('ignore_defaults')
    ignore_interdivisional = request.args.get('ignore_interdivisional')
    consolidate_results = request.args.get('consolidate_results')
    mercenary_mode = request.args.get('mercenary')


    if ignore_defaults is None:
        ignore_defaults = False

    if consolidate_results is None:
        consolidate_results = False

    if mercenary_mode is None:
        mercenary_mode = False

    pm = PersistenceManager(myapp.db_connector)
    tier = pm.get_tier_by_id(tier_id)
    return render_template('league_tier_rankings.html',
                           tier=tier,
                           consolidate_results=consolidate_results,
                           ignore_defaults=ignore_defaults,
                           ignore_interdivisional=ignore_interdivisional,
                           mercenary_mode=mercenary_mode)


@app.route("/league_players")
def league_players():
    league_id = request.args.get('league_id')
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league_by_id(league_id)
    players = []
    for tier in league.tiers:
        for player in tier.players:
            players.append(player)
            if player.division is None:
                print "wtf"
    return render_template("league_players.html", players=players, league=league)


@app.route("/add_interdivision_league_match")
def add_interdivision_league_game():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)
    league_id = league.id
    league = pm.get_league_by_id(league_id)
    tier_players = {}
    for t in league.tiers:
        players = []
        for p in t.players:
            players.append({'name': p.name, 'id': p.id})
        tier_players[t.name] = players
    return render_template("add_interdivision_league_match.html",
                           league=league,
                           tiers=league.tiers,
                           tier_players=tier_players)


@app.route("/submit_interdivisional_league_match", methods=['POST'])
def submit_interdivisional_league_match():
    player1_id = request.form['player1_dropdown']
    player2_id = request.form['player2_dropdown']
    tier_id = request.form['tier_dropdown']
    league_id = request.form['league_id']

    pm = PersistenceManager(myapp.db_connector)
    player1 = pm.get_league_player_by_id(player1_id)
    player2 = pm.get_league_player_by_id(player2_id)

    print(player1.division.get_name())
    allow_duplicate = False
    if player1.division == player2.division:
        if not player1.division.tier.get_name() == "Deep Core":
            flash("Please select two players that are not in the same division!")
            return redirect(url_for("add_interdivision_league_game",
                                    league_id=league_id))
        else:
            allow_duplicate = True

    tier = pm.get_tier_by_id(tier_id)
    now = datetime.now()


    helper = XWingVassalLeagueHelper(tier.league.name, tier.league.id)
    match = helper.create_league_match(player1.division, player1, player2, pm, allow_duplicate )
    return redirect(url_for('league_match', match_id=match.id))


@app.route("/league_admin")
def league_admin():
    return render_template('league_admin.html')


@app.route("/remove_league_player")
def remove_league_player():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)
    pm = PersistenceManager(myapp.db_connector)
    players = []
    for tier in league.tiers:
        for player in tier.players:
            players.append(player)
    return render_template("remove_league_player.html", league=league, players=players)


@app.route("/remove_league_player_form_results", methods=['POST'])
def remove_league_player_form_results():
    player_id = decode(request.form['player_dropdown'])
    league_id = decode(request.form['league_id'])

    pm = PersistenceManager(myapp.db_connector)
    player = pm.get_league_player_by_id(player_id)
    # take out their matches
    for match in player.matches:
        for subscription in match.subscriptions:
            if subscription.observer.id == player_id:
                pm.db_connector.get_session().delete(subscription)
        pm.db_connector.get_session().delete(match)
    pm.db_connector.get_session().delete(player)
    pm.db_connector.get_session().commit()
    return redirect(url_for("league_players", league_id=league_id))

@app.route("/add_league_player")
def add_league_player():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)
    tiers_divisions = {}
    tiers = []
    for tier in league.tiers:
        tiers.append(tier)
        tiers_divisions[tier.get_name()] = []
        for division in tier.divisions:
            tiers_divisions[tier.get_name()].append({'name': division.get_name(), 'id': division.id})
    return render_template('add_league_player.html', league=league, tiers_divisions=tiers_divisions, tiers=tiers)

@app.route("/add_league_player_form_results", methods=['POST'])
def add_league_player_form_results():
    player_name = decode(request.form['name'])
    email_address = decode(request.form['email_address'])
    person_name = decode(request.form['person_name'])
    division_id = request.form['division_dropdown']
    tier_id = request.form['tier_dropdown']


    pm = PersistenceManager(myapp.db_connector)

    # check to see if this player already exists
    tier_player = pm.get_league_player_by_name(player_name, tier_id)
    if tier_player is not None:  # hmm, already exists
        player_stats = tier_player.get_stats()
        return render_template("league_player.html", player=tier_player, stats=player_stats)

    tier = pm.get_tier_by_id(tier_id)
    league = tier.league
    vl = XWingVassalLeagueHelper(league.name, league.id)
    tier_player = vl.add_player(pm, division_id, tier, email_address, player_name, person_name)
    player_stats = tier_player.get_stats()
    return render_template("league_player.html", player=tier_player, stats=player_stats)

@app.route("/merge_league_divisions")
def merge_league_divisions():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)
    divisions = []
    for tier in league.tiers:
        for division in tier.divisions:
            divisions.append( {'name': division.get_name(), 'id': division.id} )
    return render_template("merge_league_divisions.html", divisions=divisions,league=league)

@app.route("/merge_league_division_form_results", methods=['POST'])
def merge_league_division_form_results():
    league_id        = decode(request.form['league_id'])
    from_division_id = decode(request.form['from_division_dropdown'])
    to_division_id   = decode(request.form['to_division_dropdown'])

    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league_by_id(league_id)
    vl = XWingVassalLeagueHelper(league.name, league.id)
    merged_division = vl.merge_divisions(pm, from_division_id, to_division_id)
    return redirect(url_for('tier_rankings', tier_id=merged_division.tier.id))


@app.route("/tier_matches")
def tier_matches():
    tier_id = request.args.get('tier_id')
    admin = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tier = pm.get_tier_by_id(tier_id)
    return render_template("tier_matches.html", tier=tier, admin=admin)

def get_league_stats(league):
    league_stats = {}
    player_stats = {}
    num_games_completed = 0
    total_games = 0
    num_lists_entered = 0
    total_num_lists = 0
    num_attachments_uploaded = 0

    # Division  |  Percent Complete  | Completed | Open
    for match_result in league.matches:
        total_games += 1
        total_num_lists += 2

        p1division = match_result.player1.division
        p2division = match_result.player2.division
        player1_division_name = p1division.get_name()
        player2_division_name = p2division.get_name()

        if not league_stats.has_key(player1_division_name):
            league_stats[player1_division_name] = {'name': player1_division_name, 'total': 0, 'complete': 0, 'open': 0}

        if not league_stats.has_key(player2_division_name):
            league_stats[player2_division_name] = {'name': player2_division_name, 'total': 0, 'complete': 0, 'open': 0}

        ls = league_stats[player1_division_name]
        ls[match_result.state] += 1
        ls['total'] += 1

        ls = league_stats[player2_division_name]
        ls[match_result.state] += 1
        ls['total'] += 1


        # Player    | Division  |  Wins   | Losses | Draws | MoV  | SoS
        player1_name = match_result.player1.get_name()
        player2_name = match_result.player2.get_name()

        if not player_stats.has_key(player1_name):
            player_stats[player1_name] = {'division': player1_division_name,
                                          'player': player1_name,
                                          'total': 0,
                                          'wins': 0,
                                          'losses': 0,
                                          'draws': 0,
                                          'MoV': 0,
                                          'SoS': 0,
                                          'points': 0}

        if not player_stats.has_key(player2_name):
            player_stats[player2_name] = {'division': player2_division_name,
                                          'player': player2_name,
                                          'total': 0,
                                          'wins': 0,
                                          'losses': 0,
                                          'draws': 0,
                                          'MoV': 0,
                                          'SoS': 0,
                                          'points': 0}

        if match_result.state == 'complete':
            num_games_completed += 1
            if match_result.player1_list:
                num_lists_entered += 1
            if match_result.player2_list:
                num_lists_entered += 1

            if match_result.challonge_attachment_url:
                num_attachments_uploaded += 1

            ps1 = player_stats[player1_name]
            ps1['total'] += 1
            ps2 = player_stats[player2_name]
            ps2['total'] += 1

            if match_result.player1_score > match_result.player2_score:  # I won!
                ps1['wins'] += 1
                diff = 100 + match_result.player1_score - match_result.player2_score
                if diff >= 12:
                    ps1['points'] += 5
                else:
                    ps1['points'] += 3
                ps1['MoV'] += diff

                # and calculate the other side it for player2
                diff = 100 - match_result.player1_score + match_result.player2_score
                ps2['losses'] += 1
                ps2['MoV'] += diff

            elif match_result.player1_score == match_result.player2_score:  # I drew!
                ps1['draws'] += 1  # and no change to MoV
                ps1['points'] += 1
                ps2['draws'] += 1  # and no change to MoV
                ps2['points'] += 1

            else:  # I lost!
                ps1['losses'] += 1
                diff = 100 - match_result.player2_score + match_result.player1_score
                ps1['MoV'] += diff

                ps2['wins'] += 1
                diff = 100 + match_result.player2_score - match_result.player1_score
                if diff >= 12:
                    ps2['points'] += 5
                else:
                    ps2['points'] += 3
                ps2['MoV'] += diff

    overall_stats = {}
    overall_stats['num_games_completed'] = num_games_completed
    overall_stats['total_games'] = total_games
    overall_stats['num_lists_entered'] = num_lists_entered
    overall_stats['total_num_lists'] = total_num_lists
    overall_stats['num_attachments_uploaded'] = num_attachments_uploaded

    return overall_stats, league_stats, player_stats

@app.route("/league")
def league_divisions():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league(CURRENT_VASSAL_LEAGUE_NAME)
    tiers = sorted(league.tiers, key= lambda x: len(x.divisions))
    #matches = pm.get_recent_league_matches(league)

    return render_template("league_s6.html",
                           league=league, tiers=tiers, session=pm.db_connector.get_session())


@app.route("/league_season_one")
def league_season_one():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league("X-Wing Vassal League Season One")
    tiers = league.tiers
    matches = pm.get_recent_league_matches(league)

    return render_template("league_s1.html",
                           league=league, tiers=tiers, matches=matches)


@app.route("/league_season_two")
def league_season_two():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league("X-Wing Vassal League Season Two")
    tiers = league.tiers
    matches = pm.get_recent_league_matches(league)

    return render_template("league_s2.html",
                           league=league, tiers=tiers, matches=matches)


@app.route("/league_season_three")
def league_season_three():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league("X-Wing Vassal League Season Three")
    tiers = league.tiers
    matches = pm.get_recent_league_matches(league)

    return render_template("league_s3.html",
                           league=league, tiers=tiers, matches=matches)


@app.route("/league_season_four")
def league_season_four():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league("X-Wing Vassal League Season Four")
    tiers = league.tiers
    matches = pm.get_recent_league_matches(league)

    return render_template("league_s4.html",
                           league=league, tiers=tiers, matches=matches)

@app.route("/league_season_five")
def league_season_five():
    pm = PersistenceManager(myapp.db_connector)
    league = pm.get_league("X-Wing Vassal League Season Five")
    tiers = league.tiers
    matches = pm.get_recent_league_matches(league)

    return render_template("league_s5.html",
                           league=league, tiers=tiers, matches=matches)

@app.route("/report_league_match")
def report_league_match():
    match_id = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    return render_template("report_league_match_form.html", match=match)

@app.route("/upload_vlog_file",methods=['POST'])
def upload_vlog_file():
    match_id = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match_id = request.form['match_id']

    match = pm.get_match(match_id)

    vlog = request.files['vlog_file']

    save_vlog(match, vlog)
    pm.db_connector.get_session().commit()
    return(redirect(url_for("league_match", match_id=match_id)))

@app.route('/upload_vlog', )
def upload_vlog():
    match_id = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)

    return render_template('upload_vlog.html', match=match)

@app.route('/download_vlog')
def download_vlog():
    match_id = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    league_id = match.tier.league.id
    return send_file(vlog_dir + "/" + str(league_id) + "/" + match.challonge_attachment_url,
                     as_attachment=True,
                     attachment_filename=match.challonge_attachment_url)


@app.route("/submit_league_match_report", methods=['POST'])
def submit_league_match_report():
    match_id = request.form['match_id']
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    player1_score = request.form['player1_score']
    player2_score = request.form['player2_score']
    winner_id = request.form['winner_id']
    match.player1_score = player1_score
    match.player2_score = player2_score
    match.winner_id = winner_id
    match.completed()

    vlog = request.files['vlog_file']
    save_vlog(match, vlog)
    pm.db_connector.get_session().commit()

    slack_notify_match_complete(match)

    return redirect(url_for('tier_matches', tier_id=match.tier_id))


def save_vlog(match, vlog):
    if vlog is not None:
        filename = vlog.filename
        if allowed_file(filename):
            try:
                filename = secure_filename(filename)
                dir = vlog_dir + "/" + str(match.tier.league.id)
                file = os.path.join(dir, filename)
                if os.path.isfile(file):  # if this file has already been uploaded ...
                    i = 1
                    done = False
                    while not done and i < 1000:
                        prefix, suffix = os.path.splitext(file)
                        prefix = prefix + str(i)
                        newfile = prefix + suffix
                        if not os.path.isfile(newfile):
                            file = newfile
                            done = True
                        else:
                            i = i + 1

                fd = open(file, 'w')
                data = vlog.read()
                fd.write(data)
                fd.close()
                dir, filename = os.path.split(file)
                url = filename
                match.challonge_attachment_url = url
            except Exception as e:
                print("Unable to upload vlog file, reason: " + str(e))


@app.route("/set_league_match_schedule")
def set_league_match_schedule():
    match_id = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    today = datetime.today().strftime('%d-%m-%Y')

    return render_template("league_match_schedule.html", match=match, today=today, timezones=common_timezones)


@app.route("/submit_league_match_schedule", methods=['POST'])
def submit_league_match_schedule():
    match_id = request.form['match_id']
    tz = request.form['timezone']
    dt = request.form['datetime12']

    fmt = '%d-%m-%Y %I:%M %p'
    datetime_obj_native = datetime.strptime(dt, fmt)
    datetime_obj_localtz = timezone(tz).localize(datetime_obj_native)

    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    match.scheduled_datetime = datetime_obj_localtz.strftime('%d-%m-%Y %I:%M %p %Z%z')
    pm.db_connector.get_session().add(match)
    pm.db_connector.get_session().commit()

    slack_notify_league_match_schedule(match)

    # finally, if the match has been escrowed, and there has been a datetime change, send it along
    if match.needs_escrow() == False:
        slack_notify_escrow_change(match, pm)
    return redirect(url_for('tier_matches', tier_id=match.tier_id))


@app.route("/escrow")
def escrow():
    match_id = request.args.get("match_id")
    player_id = request.args.get("player_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    needs_escrow = 0
    match_complete = 0
    if match.needs_escrow():
        needs_escrow = 1
    if match.is_complete():
        match_complete = 1
    if player_id is None:
        player_id = 0
    return render_template("league_escrow.html",
                           match=match,
                           selected_player_id=int(player_id),
                           needs_escrow=needs_escrow,
                           match_complete=match_complete)


def mail_escrow_complete(match, pm):
    recipients = list(ADMINS)
    if len(recipients) == 0:
        return
    for s in match.subscriptions:
        if s.notified:
            continue
        recipients.append(s.observer.email_address)
        s.notified = True
        pm.db_connector.get_session().add(s)
    pm.db_connector.get_session().commit()
    msg = Message("Escrow complete for X-Wing Vassal League match: %s v %s" % (
    match.player1.get_name(), match.player2.get_name()),
                  sender=ADMINS[0],
                  recipients=recipients)
    html = render_template("escrow_complete.html", match=match, player_id=s.observer.id)

    msg.body = 'text body'
    msg.html = html
    with app.app_context():
        mail.send(msg)


def mail_escrow_partial(player, match, pm):
    recipients = list(ADMINS)
    for s in match.subscriptions:
        if not s.partial_notified == True and s.observer.id == player.id:
            recipients.append(player.email_address)
            s.partial_notified = True
            pm.db_connector.get_session.add(s)

    if len(recipients) > 1:
        pm.db_connector.get_session().commit()

        msg = Message("Your escrow for X-Wing Vassal League match: %s v %s" % (
        match.player1.get_name(), match.player2.get_name()),
                      sender=ADMINS[0],
                      recipients=recipients)
        html = render_template("escrow_partial.html", match=match, player=player)

        msg.body = 'text body'
        msg.html = html
        with app.app_context():
            mail.send(msg)


@app.route("/force_reset_match_escrow")
def force_reset_match_escrow():
    match_id = request.args.get("match_id")  # url?arg=value

    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    match.reset_escrow()
    pm.db_connector.get_session().commit()
    return redirect(url_for('escrow', match_id=match_id, player_id=match.player1_id))


@app.route("/reset_match_escrow")
def reset_match_escrow():
    match_id = request.args.get("match_id")
    player_id = request.args.get("player_id")

    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    match.delete_partial_escrow(player_id)
    pm.db_connector.get_session().commit()
    return redirect(url_for('escrow', match_id=match_id, player_id=player_id))

def slack_notify_match_complete(match):
    js = {
        'url' : match.get_url(use_markup=False),
        'player1': {
            'name': match.player1.name,
            'division_name': match.player1.division.name,
            'points_destroyed': match.player1_score,
            'mov': match.player1.get_mov(match)
        },
        'player2': {
            'name': match.player2.name,
            'division_name': match.player2.division.name,
            'points_destroyed': match.player2_score,
            'mov': match.player2.get_mov(match)
        },
        'winner': match.get_winner().name,
        'tier_name': match.tier.name
    }
    jsondata = json.dumps(js)
    print jsondata
    resp = post("https://cv6jcoop2e.execute-api.us-east-1.amazonaws.com/prod/match-completed",
                data=jsondata)
    print "posted, got response %d " % (resp.status_code)
    return resp.status_code


def slack_notify_league_match_schedule(match):
    js = {
        'scheduled_datetime': match.scheduled_datetime,
        'tier_name': match.tier.name,
        'player1': {
            "name": match.player1.name,
            "division_name": match.player1.division.name,
        },
        'player2': {
            "name": match.player2.name,
            "division_name": match.player2.division.name,
        },
        "url": match.get_url(use_markup=False)
    }

    jsondata = json.dumps(js)
    print jsondata
    resp = post("https://cv6jcoop2e.execute-api.us-east-1.amazonaws.com/prod/match-scheduled",
                data=jsondata)
    print "posted, got response %d " % (resp.status_code)
    return resp.status_code

def slack_notify_escrow_change(match, pm):
    if match.slack_notified:
        return
    tier = match.tier
    player1 = match.player1
    player2 = match.player2
    c = XWSListConverter(match.player1_list)
    p1_xws = c.data
    c = XWSListConverter(match.player2_list)
    p2_xws = c.data
    js = {"tier_name": tier.name,
          "scheduled_datetime": match.scheduled_datetime,
          "url": match.get_url(use_markup=False),
          "player1": {
              "name": player1.name,
              "division_name": player1.division.name,
              "list": match.player1_list_url,
              "pretty_print": match.player1_list.pretty_print_list('\n'),
              "xws": p1_xws
          },
          "player2": {
              "name": player2.name,
              "division_name": player2.division.name,
              "list": match.player2_list_url,
              "pretty_print": match.player2_list.pretty_print_list('\n'),
              "xws": p2_xws
          }
          }
    jsondata = json.dumps(js)
    resp = post("https://cv6jcoop2e.execute-api.us-east-1.amazonaws.com/prod/escrow-notify",
                data=jsondata)
    print "posted, got response %d " % (resp.status_code)
    if resp.status_code == 200:
        # posted good
        match.slack_notified = True
        pm.db_connector.get_session().add(match)
        pm.db_connector.get_session().commit()

    return resp.status_code


@app.route("/escrow_change")
def escrow_change():
    match_id = request.args.get("match_id")
    player_id = request.args.get("player_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    escrow_complete = 1
    if match.needs_escrow():
        escrow_complete = 0
        player = match.partial_escrow()
        if player:
            mail_escrow_partial(player, match, pm)

    if escrow_complete:
        try:
            slack_notify_escrow_change(match, pm)
            mail_escrow_complete(match, pm)
        except Exception as inst:
            print "unable to send out escrow email, reason: %s" % (inst)

    response = jsonify(player1_list=match.get_player1_escrow_text(),
                       player2_list=match.get_player2_escrow_text(),
                       player1_id=match.player1_id,
                       player2_id=match.player2_id,
                       player_id=player_id,
                       escrow_complete=escrow_complete)
    return response

@app.route("/league_match", methods=['GET'])
def league_match():
    match_id  = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    return render_template('league_match.html', match=match)

@app.route("/delete_match", methods=['GET'])
def delete_match():
    match_id = request.args.get("match_id")
    pm = PersistenceManager(myapp.db_connector)
    match = pm.get_match(match_id)
    tier = match.tier

    pm.db_connector.get_session().delete(match)
    pm.db_connector.get_session().commit()

    return render_template("tier_matches.html", tier=tier)


urlregex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@app.route("/escrow_list_url", methods=['POST'])
def escrow_list_url():
    player_list_url = request.args.get("player_list_url")
    player_id = int(request.args.get("player_id"))
    match_id = request.args.get("match_id")
    # try to figure out what sort of url it is
    match = urlregex.match(player_list_url)
    if match is None:
        response = jsonify(message="That is not a url!  Please provide a valid YASB, voidstate, or FABs url")
        response.status_code = (500)
        return response
    else:
        try:
            xws = GeneralXWSFetcher().fetch(player_list_url)
            if xws is None:
                response = jsonify(message="That is not a valid YASB, voidstate, or FABs url!")
                response.status_code = (500)
                return response
            else:
                converter = XWSToJuggler(xws)
                pm = PersistenceManager(myapp.db_connector)
                match = pm.get_match(match_id)
                archtype, first_time_archtype_seen = converter.convert(pm)
                match.set_archtype(player_id, archtype)
                match.set_url(player_id, player_list_url)
                pm.commit()

                list_link = match.get_player_list_url(player_id)
                list_text = archtype.pretty_print_list()

                archtype_tourney_count = pm.archtype_tourney_count(archtype)
                archtype_league_count = pm.archtype_league_count(archtype)

                return jsonify(archtype_tourney_count=archtype_tourney_count,
                               archtype_league_count=archtype_league_count,
                               archtype_url=url_for("archtype", id=archtype.id),
                               total_count=archtype_tourney_count + archtype_league_count,
                               was_original=first_time_archtype_seen,
                               list_text=list_text,
                               list_link=list_link,
                               player_id=player_id,
                               match_id=match_id)
        except Exception as err:
            message = "unable to fetch list, reason: " + str(err)
            response = jsonify(message=message)
            response.status_code = (500)
            return response


@app.route("/search")
def versus():
    return render_template("search_versus.html", url_root=request.url_root)


@app.route("/search_guide")
def search_guide():
    return render_template("search_guide.html")


def merge_versus_results(pm, search_results1, search_results2):
    s1_archtypes = {}
    s2_archtypes = {}

    results = []
    # grab all the unique archtypes
    for tl in search_results1:
        archtype_id = tl.archtype_id
        if not s1_archtypes.has_key(archtype_id):
            s1_archtypes[archtype_id] = []
        s1_archtypes[archtype_id].append(tl)

    for tl in search_results2:
        archtype_id = tl.archtype_id
        if not s2_archtypes.has_key(archtype_id):
            s2_archtypes[archtype_id] = []
        s2_archtypes[archtype_id].append(tl)

    merged_results = pm.get_merged_search_results(s1_archtypes.keys(), s2_archtypes.keys())
    return merged_results


@app.route("/search_results", methods=['POST'])
def get_search_results():
    try:
        search_text = request.json['search-text']
        s = Search(search_text)
        results = s.search()
        return render_template('search_results.html', results=results, url_root=request.url_root), 200
    except ValueError, e:
        return render_template('search_error.html', errortext=str(e))


@app.route("/search_versus_results", methods=['POST'])
def get_search_versus_results():
    try:
        search1_text = request.json['search1-text']
        search2_text = request.json['search2-text']
        versus_enabled = request.json['versus-enabled']
        pm = PersistenceManager(myapp.db_connector)
        results = None
        if versus_enabled:
            s1 = Search(search1_text)
            s2 = Search(search2_text)
            r1 = s1.search()
            r2 = s2.search()
            results = merge_versus_results(pm, r1, r2)
            return render_template('search_versus_results.html',
                                   versus_enabled=versus_enabled,
                                   results=results,
                                   s1=search1_text,
                                   s2=search2_text,
                                   url_root=request.url_root), 200

        else:
            s = Search(search1_text)
            results = s.search()
            return render_template('search_results.html', versus_enabled=versus_enabled, results=results,
                                   url_root=request.url_root), 200
    except ValueError, e:
        return render_template('search_error.html', errortext=str(e))


@app.route("/events")
def events():
    events = PersistenceManager(myapp.db_connector).get_events()
    return render_template("event.html", events=events)


@app.route("/tourney_admin")
def tourney_admin():
    tourneys = PersistenceManager(myapp.db_connector).get_tourneys()
    return render_template("tourney_admin.html", tourneys=tourneys)



@app.route("/tourneys_page")
def tourneys_page():
    columns = [
        ColumnDT(sqlalchemy.cast(Tourney.tourney_date, Date)),
        ColumnDT(Tourney.tourney_name),
        ColumnDT(Tourney.id),
        ColumnDT(TourneyVenue.venue),
        ColumnDT(TourneyVenue.id),
        ColumnDT(TourneyVenue.city + "/" + TourneyVenue.state + "/" + TourneyVenue.country),
        ColumnDT(Tourney.participant_count),
        ColumnDT(Tourney.tourney_type),
        ]
    query = myapp.db_connector.get_session().query().select_from(Tourney).join(TourneyVenue)
    params = request.args.to_dict()

    rowtable = DataTables(params, query, columns)
    result = rowtable.output_result()

    return jsonify(result)


@app.route("/tourneys")
def tourneys():
    admin_on = request.args.get('admin')
    if admin_on is not None:
        admin_on = True
    else:
        admin_on = False
    return render_template('tourneys.html', admin=admin_on)


@app.route("/tourney_results")
def get_tourney_results():
    tourney_id = request.args.get('tourney_id')
    return redirect(url_for('get_tourney_details', tourney_id=tourney_id))


@app.route("/archtypes")
def archtypes():
    archtypes = simple_cache.get('archtypes')
    if archtypes is None:
        pm = PersistenceManager(myapp.db_connector)
        archtypes = pm.get_ranked_archtypes(request.url_root)
        simple_cache.set('archtypes', archtypes, timeout=60 * 60 * 12)
    return render_template("archtypes.html", archtypes=archtypes)


def get_results_for_archtype(pm, archtype_id):
    lists = pm.get_lists_for_archtype(archtype_id)
    results = []
    ret = {}
    ret['pretty_print'] = lists[0][0].pretty_print(manage_list=0, show_results=0, manage_archtype=0,
                                                   url_root=request.url_root)
    for listpair in lists:
        list = listpair[0]
        res = pm.get_round_results_for_list(list.id)
        for r in res:
            results.append(r)
    ret["results"] = results
    return ret


@app.route("/archtype")
def archtype():
    archtype_id = request.args.get('id')
    pm = PersistenceManager(myapp.db_connector)
    archtype = pm.get_archtype(archtype_id)
    stats = archtype.get_performance_stats(pm, request.url_root)
    all_tags = pm.get_all_tags()
    if all_tags is None:
        all_tags = []

    archtype_match_results = get_results_for_archtype(pm, archtype_id)
    return render_template("archtype.html",
                           stats=stats,
                           archtype=archtype,
                           archtype_id=archtype.id,
                           all_tags=all_tags,
                           archtype_match_results=archtype_match_results,
                           url_root=request.url_root)


@app.route("/add_tag", methods=['POST'])
def add_tag():
    data = request.json['data']
    archtype_id = data['archtype_id']
    tag_text = data['tag']

    pm = PersistenceManager(myapp.db_connector)
    archtype = pm.get_archtype(archtype_id)
    pm.add_tag(archtype, tag_text)

    update_archtypes_cache(archtype)
    return jsonify({"success": 1})


def update_archtypes_cache(archtype):
    archtypes = simple_cache.get('archtypes')
    if archtypes is None:
        pm = PersistenceManager(myapp.db_connector)
        archtypes = pm.get_ranked_archtypes(request.url_root)
    i = 0
    for a in archtypes:
        if a[0] == archtype.id:
            a[3] = archtype.pretty_print_tags()
            archtypes[i] = a
            simple_cache.set('archtypes', archtypes, timeout=60 * 60 * 12)
            break
        i = i + 1


@app.route("/remove_tag", methods=['POST'])
def remove_tag():
    data = request.json['data']
    archtype_id = data['archtype_id']
    tag_text = data['tag']

    pm = PersistenceManager(myapp.db_connector)
    archtype = pm.get_archtype(archtype_id)
    pm.remove_tag(archtype, tag_text)
    update_archtypes_cache(archtype)
    return jsonify({"success": 1})


@app.route("/update_tourney_details/", methods=['POST'])
def update_tourney_details():
    tourney_id = request.form['tourney_id']
    name = decode(request.form['name'])
    type = request.form['tourney_type']
    print request.form['datepicker']
    mmddyyyy = request.form['datepicker']
    fmt = '%m/%d/%Y'
    date = datetime.strptime(mmddyyyy, fmt)
    round_length = request.form['round_length_userdef']
    tourney_format_def = request.form['tourney_format_dropdown']
    tourney_format_custom = request.form['tourney_format_custom']
    participant_count = int(request.form['participant_count'])
    country = decode(request.form['country'])
    state = decode(request.form['state'])
    city = decode(request.form['city'])
    venue = decode(request.form['venue'])
    video_url = request.form['video_url']

    tourney_format = None
    if tourney_format_def is None or len(tourney_format_def) == 0:
        if tourney_format_custom is None or len(tourney_format_custom) == 0:
            tourney_format = xwingmetadata.format_default
        else:
            tourney_format = decode(tourney_format_custom)
    else:
        tourney_format = str(tourney_format_def)

    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)

    tourney.tourney_name = name
    tourney.tourney_type = type
    tourney.tourney_date = date
    tourney.round_length = round_length
    tourney.format = tourney_format
    tourney.participant_count = participant_count

    if tourney.venue is None:
        tourney.venue = pm.get_tourney_venue(country, state, city, venue)

    tourney.venue.country = country
    tourney.venue.state = state
    tourney.venue.city = city
    tourney.venue.venue = venue

    if video_url is not None:
        tourney.video_url = video_url

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="edit tourney information",
                  event_details="edited " + name)

    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return redirect(url_for('get_tourney_details', tourney_id=tourney_id))


@app.route("/get_tourney_details")
def get_tourney_details():
    tourney_id = request.args.get('tourney_id')

    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)

    unlocked = True
    if tourney.locked:
        unlocked = False

    return render_template('edit_tourney.html', tourney_id=tourney_id,
                           tourney=tourney,
                           unlocked=unlocked)


def create_default_editor_ranking(i, row):
    row['player_id'] = None
    row['player_name'] = 'Player%d' % (i)
    row['score'] = 0
    row['swiss_rank'] = i
    row['dropped'] = False
    row['championship_rank'] = None
    row['mov'] = 0
    row['sos'] = 0


@app.route("/get_rankings")
def get_tourney_data():
    tourney_id = request.args['tourney_id']
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)

    de = RankingEditor(pm, tourney, url_root=request.url_root)
    return de.get_json()


@app.route("/get_pre_elim_results")
def get_pre_elim_results():
    tourney_id = request.args['tourney_id']
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)
    er = RoundResultsEditor(pm, tourney, pre_elim=True, url_root=request.url_root)
    json_ret = er.get_json()
    return json_ret


@app.route("/get_elim_results")
def get_elim_results():
    tourney_id = request.args['tourney_id']
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)
    er = RoundResultsEditor(pm, tourney, pre_elim=False, url_root=request.url_root)
    json_ret = er.get_json()
    return json_ret


@app.route("/edit_rankings", methods=['POST'])
def edit_ranking_row():
    # see https://editor.datatables.net/manual/server
    tourney_id = request.args['tourney_id']
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)

    de = RankingEditor(pm, tourney, url_root=request.url_root)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="edit ranking row")

    player_name = request.values['data[player_name]']
    player_name = decode(player_name)
    ret = de.set_and_get_json(request, player_name, event)
    event.event_details = event.event_details + " in tourney " + tourney.tourney_name
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()
    return ret


def edit_results(request, pre_elim=True):
    # see https://editor.datatables.net/manual/server
    tourney_id = request.args['tourney_id']
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)

    rre = RoundResultsEditor(pm, tourney, request.url_root, pre_elim)
    ret = rre.get_and_set_json(request)
    return ret


@app.route("/edit_pre_elim_results", methods=['POST'])
def edit_pre_elim_results():
    return edit_results(request, True)


@app.route("/edit_elim_results", methods=['POST'])
def edit_elim_results():
    # see https://editor.datatables.net/manual/server
    return edit_results(request, True)


@app.route("/new")
def new():
    set = sorted(xwingmetadata.sets_and_expansions.keys())
    pm = PersistenceManager(myapp.db_connector)
    venues = pm.get_tourney_venues()
    return render_template('new_tourney.html', sets=set,
                           tourney_formats=xwingmetadata.formats,
                           format_default=xwingmetadata.format_default,
                           venues=venues)


@app.route("/edit_tourney_details")
def edit_tourney_details():
    tourney_id = request.args.get('tourney_id')

    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)
    venues = pm.get_tourney_venues()
    tourney_date = tourney.tourney_date
    date_str = "%d/%d/%d" % (tourney_date.month, tourney_date.day, tourney_date.year)
    print "tourney date is " + date_str

    return render_template('edit_tourney_details.html', tourney_id=tourney_id,
                           tourney=tourney,
                           venues=venues,
                           tourney_formats=xwingmetadata.formats,
                           tourney_date=date_str,
                           unlocked=False)


def generate(rows):
    for r in rows:
        yield ",".join(r) + "\n"


def get_tourney_lists_as_text(tourney, make_header=True):
    rows = []
    header = xwingmetadata.header()

    if make_header:
        rows.append(header)

    tourney_date = "%d/%d/%d" % (tourney.tourney_date.month, tourney.tourney_date.day, tourney.tourney_date.year)
    row_defaults = [tourney.tourney_name.replace(',', ' '), tourney.tourney_type, tourney_date]

    for tourney_list in tourney.tourney_lists:
        if tourney_list.ships() is None or len(tourney_list.ships()) == 0:
            new_row = []
            new_row.extend(row_defaults)
            for i in range(len(new_row), len(header)):
                if header[i] == 'player' and tourney_list.player.player_name is not None: #little hack for player name
                    new_row.append(tourney_list.player.player_name)
                else:
                    new_row.append('')
            rows.append(new_row)
        else:
            for ship in tourney_list.ships():
                new_row = []
                new_row.extend(row_defaults)
                new_row.extend([tourney_list.player.player_name.replace(',', ' '),
                                tourney_list.faction().description,
                                str(tourney_list.points()),
                                str(tourney_list.player.result.rank),
                                str(tourney_list.player.result.elim_rank),
                                str(tourney_list.id),
                                ship.ship_pilot.ship_type.description,
                                ship.ship_pilot.pilot.name
                                ])

                for i in range(len(new_row), len(header)):
                    new_row.append(ship.get_upgrade(header[i]))

                rows.append(new_row)
    return rows


def csv_response(rows, name):
    disposition = "attachment; filename=" + name
    return Response(generate(rows), mimetype='text/csv', headers={'Content-Disposition': disposition})


@app.route("/export_all_lists")
def export_all_lists():
    pm = PersistenceManager(myapp.db_connector)
    tourneys = pm.get_tourneys();
    make_header = True
    rows = []
    for tourney in tourneys:
        ret = get_tourney_lists_as_text(tourney, make_header)
        make_header = False
        rows.extend(ret)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="export all tourney lists")
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()
    return csv_response(rows, "all_lists_download.csv")


@app.route("/export_tourney_lists")
def export_tourney_lists():
    tourney_id = request.args.get('tourney_id')
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)

    ret = get_tourney_lists_as_text(tourney)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="export tourney lists",
                  event_details="exported tourney %s" % (tourney.tourney_name))
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return csv_response(ret, "tourney_list_download.csv")


@app.route("/delete_tourney")
def delete_tourney():
    tourney_id = request.args.get('tourney')
    pm = PersistenceManager(myapp.db_connector)
    pm.delete_tourney_by_id(tourney_id)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="delete tourney",
                  event_details="deleted tourney %s" % (tourney_id))
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return redirect(url_for('tourneys'))


def add_sets_and_venue_to_tourney(city, country, pm, sets_used, state, t, venue):
    # load in the sets used
    if sets_used:
        for set_name in sets_used:
            set = pm.get_set(set_name)
            if set is not None:
                ts = TourneySet(tourney=t, set=set)
                pm.db_connector.get_session().add(ts)
    tv = pm.get_tourney_venue(country=country, state=state, city=city, venue=venue)
    t.venue = tv
    pm.db_connector.get_session().add(tv)


def create_tourney(cryodex, tourney_name, tourney_date, tourney_type,
                   round_length, sets_used, country, state, city, venue, email, participant_count, tourney_format, video_url):
    pm = PersistenceManager(myapp.db_connector)
    t = Tourney(tourney_name=tourney_name, tourney_date=tourney_date,
                tourney_type=tourney_type, round_length=round_length, email=email, entry_date=datetime.now(),
                participant_count=participant_count, locked=False, format=tourney_format, video_url=video_url)

    pm.db_connector.get_session().add(t)
    # add the players
    players = {}
    lists = {}

    for player in cryodex.players.keys():
        tp = TourneyPlayer(tourney=t, player_name=player)
        tlist = TourneyList(tourney=t, player=tp)
        pm.db_connector.get_session().add(tlist)
        players[player] = tp
        lists[player] = tlist

    pm.db_connector.get_session().commit()

    for round_type in cryodex.rounds.keys():
        rounds = cryodex.rounds[round_type]
        for round in rounds:
            tr = TourneyRound(round_num=int(round.number), round_type=round.get_round_type(), tourney=t)
            pm.db_connector.get_session().add(tr)
            for round_result in round.results:
                rr = None
                if round_result.bye:
                    p1_tourney_list = lists[round_result.player1]
                    rr = RoundResult(round=tr, list1=p1_tourney_list, list2=None, winner=None, loser=None,
                                     list1_score=None,
                                     list2_score=None, bye=round_result.bye, draw=round_result.draw)
                else:
                    p1_tourney_list = lists[round_result.player1]
                    p2_tourney_list = None
                    p2_tourney_list = lists[round_result.player2]
                    winner = None
                    loser = None
                    if round_result.player1 == round_result.winner:
                        winner = p1_tourney_list
                        loser = p2_tourney_list
                    else:
                        winner = p2_tourney_list
                        loser = p1_tourney_list

                    rr = RoundResult(round=tr, list1=p1_tourney_list, list2=p2_tourney_list, winner=winner, loser=loser,
                                     list1_score=round_result.player1_score,
                                     list2_score=round_result.player2_score, bye=round_result.bye,
                                     draw=round_result.draw)
                pm.db_connector.get_session().add(rr)

    add_sets_and_venue_to_tourney(city, country, pm, sets_used, state, t, venue)

    # finally load the rankings
    for rank in cryodex.ranking.rankings:
        r = TourneyRanking(tourney=t,
                           player=players[rank.player_name],
                           rank=rank.rank,
                           elim_rank=rank.elim_rank,
                           mov=rank.mov,
                           sos=rank.sos,
                           score=rank.score,
                           dropped=rank.dropped)
        pm.db_connector.get_session().add(r)
        pm.db_connector.get_session().commit()
        if rank.list_id is not None and len(rank.list_id) > 0:
            # cryodex provided a list id ... load it
            try:
                tourney_list = lists[rank.player_name]
                fetcher = VoidStateXWSFetcher()
                xws = fetcher.fetch(rank.list_id)
                converter = XWSToJuggler(xws)
                converter.convert(pm, tourney_list)

            except Exception as err:
                mail_error(errortext=str(err) + "<br><br>Unable to fetch list id " + rank.list_id + " from voidstate")



    # and commit all the work
    pm.db_connector.get_session().commit()
    return t


def save_cryodex_file(failed, filename, data):
    dir = None
    if failed:
        dir = os.path.join(static_dir, "cryodex/fail")
    else:
        dir = os.path.join(static_dir, "cryodex/success")
    file = os.path.join(dir, filename)
    fd = open(file, 'w')
    fd.write(data.encode('utf8'))
    fd.close()


@app.route("/store_champs")
def store_champs():
    store_champs = simple_cache.get('store-champ-data')
    if store_champs is None:
        pm = PersistenceManager(myapp.db_connector)
        tourneys = pm.get_tourneys()
        store_champs = []
        for tourney in tourneys:
            for rank in tourney.rankings:
                if tourney.is_store_championship():
                    rec = {'tourney': decode(tourney.tourney_name),
                           'num_participants': tourney.participant_count,
                           'player': decode(rank.player.player_name),
                           'swiss_standing': rank.rank,
                           'championship_standing': rank.elim_rank,
                           'pretty_print': rank.pretty_print()}
                    store_champs.append(rec)

        simple_cache.set('store-champ-data', store_champs, timeout=5 * 60)

    return render_template('store_champ_lists.html', championship_lists=store_champs)


@app.route("/add_tourney", methods=['POST'])
def add_tourney():
    # TODO: better edge testing against user input
    name = decode(request.form['name'])
    email = decode(request.form['email'])
    type = request.form['tourney_type']

    mmddyyyy = request.form['datepicker']
    fmt = '%m/%d/%Y'
    date = datetime.strptime(mmddyyyy, fmt)

    round_length_dropdown = request.form['round_length_dropdown']
    round_length_userdef = request.form['round_length_userdef']
    tourney_format_def = request.form['tourney_format_dropdown']
    tourney_format_custom = request.form['tourney_format_custom']
    participant_count = int(request.form['participant_count'])
    sets_used = request.form.getlist('sets[]')
    country = decode(request.form['country'])
    state = decode(request.form['state'])
    city = decode(request.form['city'])
    venue = decode(request.form['venue'])
    video_url = request.form['video_url']

    round_length = None
    if round_length_dropdown is None or len(round_length_dropdown) == 0:
        round_length = int(round_length_userdef)
    else:
        round_length = int(round_length_dropdown)

    tourney_format = None
    if tourney_format_def is None or len(tourney_format_def) == 0:
        if tourney_format_custom is None or len(tourney_format_custom) == 0:
            tourney_format = xwingmetadata.format_default
        else:
            tourney_format = decode(tourney_format_custom)
    else:
        tourney_format = str(tourney_format_def)

    tourney_report = request.files['tourney_report']

    mail_message("New tourney creation attempt",
                 "Request to create tourney name %s from user %s of type %s on day %s with %d participants" % \
                 (name, email, type, date, participant_count))

    if tourney_report:
        filename = tourney_report.filename
        data = None
        if tourney_report and allowed_file(filename):
            try:
                data = tourney_report.read()
                data = decode(data)
                cryodex = Cryodex(data, filename)
                t = create_tourney(cryodex, name, date, type, round_length,
                                   sets_used, country, state, city, venue, email, participant_count, tourney_format, video_url)
                sfilename = secure_filename(filename) + "." + str(t.id)
                save_cryodex_file(failed=False, filename=sfilename, data=data)

                event = Event(remote_address=myapp.remote_address(request),
                              event_date=func.now(),
                              event="create tourney",
                              event_details="created tourney %s from croydex input" % (t.tourney_name))
                pm = PersistenceManager(myapp.db_connector)
                pm.db_connector.get_session().add(event)
                pm.db_connector.get_session().commit()
                mail_message("New cryodex tourney created",
                             "A new tourney named '%s' with id %d was created from file %s!" % (
                             t.tourney_name, t.id, filename))
                print "getting tourney details"
                return redirect(url_for('get_tourney_details', tourney_id=t.id))
            except (Exception, UnicodeEncodeError) as err:
                filename = str(uuid.uuid4()) + ".html"
                save_cryodex_file(failed=True, filename=filename, data=data)
                mail_error(errortext=str(err) + "<br><br>Filename =" + filename)
                return render_template('tourney_entry_error.html', errortext=str(err))


    else:  # user didnt provide a cryodex file ... have to do it manually
        try:
            pm = PersistenceManager(myapp.db_connector)
            t = Tourney(tourney_name=name, tourney_date=date, tourney_type=type, locked=False,
                        round_length=round_length, email=email, entry_date=datetime.now(),
                        participant_count=participant_count, format=tourney_format, video_url=video_url)
            pm.db_connector.get_session().add(t)
            add_sets_and_venue_to_tourney(city, country, pm, sets_used, state, t, venue)
            pm.db_connector.get_session().commit()
            event = Event(remote_address=myapp.remote_address(request),
                          event_date=func.now(),
                          event="create tourney",
                          event_details="created tourney %s from manual input" % (t.tourney_name))
            pm = PersistenceManager(myapp.db_connector)
            pm.db_connector.get_session().add(event)
            pm.db_connector.get_session().commit()
            mail_message("New manual tourney created",
                         "A new tourney named '%s' with id %d was created!" % (t.tourney_name, t.id))
            return redirect(url_for('get_tourney_details', tourney_id=t.id))
        except Exception as err:
            mail_error(errortext=str(err))
            return render_template('tourney_entry_error.html', errortext=str(err))



            # TODO: this is code for handling the scanned player list scenario.   I'll refactor it to something useful if the situation comes up again.
            # load all the files in the folder
            # folder_path = os.path.join(static_dir, folder)
            # tourney_files = {}
            # for f in os.listdir(folder_path):
            #     if isfile(os.path.join(folder_path,f)):
            #         player_name = os.path.splitext(f)[0]
            #         tourney_files[player_name] = UPLOAD_FOLDER +  "/" + folder + "/" + f
            # lists   = []
            # for player_name in tourney_files.keys():
            #     f = tourney_files[player_name]
            #
            #     try:
            #
            #         match = re.match(r'^(.*?)\s+(\d+)',player_name)
            #
            #         tourney_list = TourneyList( tourney_id=tourney.id,
            #                                     image=f,
            #                                     player_name=match.group(1),
            #                                     tourney_standing=match.group(2))
            #         lists.append( tourney_list )
            #     except:
            #         print ("unable to load file name %s" % ( player_name ))

            # myapp.db_connector.get_session().add_all( lists )
            # myapp.db_connector.get_session().commit()


@app.route("/browse_list")
def browse_list():
    tourney_name = request.args.get('tourney')
    admin = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney(tourney_name)
    tourney_lists = tourney.tourney_lists
    return render_template('tourney_lists.html', tourney=tourney, tourney_lists=tourney_lists, admin=admin)


# WTF googlebot?
@app.route("/delete_list_and_retry_list_entry")
def delete_list_and_retry():
    tourney_list_id = request.args.get('tourney_list_id')
    print("calling delete list and retry on tourney id " + tourney_list_id)

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    pm.delete_tourney_list_details(tourney_list)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="delete list",
                  event_details="deleted list id %d from tourney %s" % (
                  tourney_list.id, tourney_list.tourney.tourney_name))
    pm = PersistenceManager(myapp.db_connector)
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return redirect(url_for('enter_list', tourney=tourney_list.tourney.id, tourney_list_id=tourney_list.id))


@app.route("/success")
def success():
    tourney_name = request.args.get("tourney_name")
    return render_template("success_kid.html", tourney_name=tourney_name)


@app.route("/enter_list")
def enter_list():
    tourney_id = request.args.get('tourney_id')
    tourney_list_id = request.args.get('tourney_list_id')

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = None
    tourney = None

    if tourney_list_id is None:
        tourney = pm.get_tourney_by_id(tourney_id)
        tourney_list = pm.get_random_tourney_list(tourney)
        if tourney_list is None:
            return redirect(url_for("success", tourney_name=tourney.tourney_name))
    else:
        tourney_list = pm.get_tourney_list(tourney_list_id)
        tourney = tourney_list.tourney

    m = xwingmetadata.XWingMetaData()

    image_src = None
    if tourney_list.image is not None:
        image_src = urllib.quote(tourney_list.image)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="create list",
                  event_details="created list %d for tourney %s" % (tourney_list.id, tourney.tourney_name))
    pm = PersistenceManager(myapp.db_connector)
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return render_template('list_entry.html',
                           meta=m,
                           image_src=image_src,
                           tourney_list=tourney_list,
                           tourney_list_id=tourney_list.id,
                           tourney_id=tourney.id,
                           tourney=tourney)


@app.route("/get_summaries")
def get_summaries():
    try:
        summaries = simple_cache.get('banner-summary-data')
        if summaries is None:
            pm = PersistenceManager(myapp.db_connector)
            summaries = pm.get_summaries()
            simple_cache.set('banner-summary-data', summaries, timeout=5 * 60)
        return json.dumps(summaries)
    except Exception, e:
        response = jsonify(message=str(e))
        response.status_code = (500)
        return response


@app.route("/get_from_fab", methods=['POST'])
def get_from_fab():
    try:
        fab = request.args.get('fab')
        tourney_id = request.args.get('tourney_id')
        tourney_list_id = request.args.get('tourney_list_id')
        pm = PersistenceManager(myapp.db_connector)
        tourney_list = pm.get_tourney_list(tourney_list_id)

        fetcher = FabFetcher()
        xws = fetcher.fetch(fab)
        converter = XWSToJuggler(xws)
        converter.convert(pm, tourney_list)
        pm.db_connector.get_session().commit()
        return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list_id)
    except Exception, e:
        mail_error(
            "Unable to fetch list for tourney " + str(tourney_id) + " from fab for url " + fab + ", reason: " + str(e))
        response = jsonify(message=str(e))
        response.status_code = (500)
        return response


@app.route("/mysql")
def mysql():
    print "trying to fetch prod.sql from mysqldb endpoint"
    return url_for('static', filename='prod.sql')


@app.route("/get_from_yasb", methods=['POST'])
def get_from_yasb():
    try:
        yasb = request.args.get('yasb')
        tourney_id = request.args.get('tourney_id')
        tourney_list_id = request.args.get('tourney_list_id')
        pm = PersistenceManager(myapp.db_connector)
        tourney_list = pm.get_tourney_list(tourney_list_id)

        fetcher = YASBFetcher()
        xws = fetcher.fetch(yasb)
        converter = XWSToJuggler(xws)
        converter.convert(pm, tourney_list)

        pm.db_connector.get_session().commit()
        return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list_id)
    except Exception, e:
        mail_error(
            "Unable to fetch from yasb for tourney " + str(tourney_id) + " for id " + yasb + ", reason: " + str(e))
        response = jsonify(message=str(e))
        response.status_code = (500)
        return response


@app.route("/get_from_voidstate", methods=['POST'])
def add_from_voidstate():
    try:
        voidstate_id = request.args.get('voidstate_id')
        tourney_id = request.args.get('tourney_id')
        tourney_list_id = request.args.get('tourney_list_id')

        pm = PersistenceManager(myapp.db_connector)
        tourney_list = pm.get_tourney_list(tourney_list_id)

        fetcher = VoidStateXWSFetcher()
        xws = fetcher.fetch(voidstate_id)
        converter = XWSToJuggler(xws)
        converter.convert(pm, tourney_list)
        pm.db_connector.get_session().commit()
        return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list.id)
    except Exception, e:
        mail_error("Unable to fetch for tourney " + str(
            tourney_id) + " from voidstate for id " + voidstate_id + ", reason: " + str(e))
        response = jsonify(message=str(e))
        response.status_code = (500)
        return response


@app.route("/unlock_tourney", methods=['POST'])
def unlock_tourney():
    key = request.args.get('key')
    tourney_id = request.args.get('tourney_id')
    pm = PersistenceManager(myapp.db_connector)
    state = ""
    try:
        tourney = pm.get_tourney_by_id(tourney_id)
        if len(key) and tourney.email == key:
            response = jsonify(result="success")
            if tourney.locked == True:  # flip the lock
                tourney.locked = False
                state = "unlocked"
            else:
                tourney.locked = True
                state = "locked"
            event = Event(remote_address=myapp.remote_address(request),
                          event_date=func.now(),
                          event="lock/unlock tourney",
                          event_details="set tourney %s to state %s" % (tourney.tourney_name, state))
            pm.db_connector.get_session().add(event)
            pm.db_connector.get_session().commit()
            return response
        else:
            response = jsonify(result="fail")
            return response
    except Exception, e:
        error = "someone tried to unlock tourney_id " + tourney_id + " with email address " + key + " ( expected " + tourney.email + " ) "
        mail_error(error)
        response = jsonify(message=str(e))
        response.status_code = (500)
        return response


@app.route("/add_squad", methods=['POST'])
def add_squad():
    data = request.json['data']
    points = request.json['points']
    faction = request.json['faction']

    tourney_id = request.args.get('tourney_id')
    tourney_list_id = request.args.get('tourney_list_id')

    pm = PersistenceManager(myapp.db_connector)

    ships = []
    for squad_member in data:
        ship_pilot = pm.get_ship_pilot(squad_member['ship'], squad_member['pilot'])
        ship = Ship(ship_pilot_id=ship_pilot.id, ship_pilot=ship_pilot)
        for upgrade in squad_member['upgrades']:
            upgrade = pm.get_upgrade(upgrade['type'], upgrade['name'])
            ship_upgrade = ShipUpgrade(ship_id=ship.id,
                                       upgrade=upgrade)
            ship.upgrades.append(ship_upgrade)
        ships.append(ship)

    hashkey = ArchtypeList.generate_hash_key(ships)

    archtype = pm.get_archtype_by_hashkey(hashkey)

    if archtype is None:
        # ding ding!
        # we've never seen this list before!
        archtype = ArchtypeList()
        pm.db_connector.get_session().add(archtype)
        archtype.ships = ships
        for ship in ships:
            ship.archtype = archtype
            pm.db_connector.get_session().add(ship)
        archtype.faction = Faction.from_string(faction)
        archtype.points = int(points)
        archtype.pretty = archtype.pretty_print_list()
        pm.db_connector.get_session().commit()

    tourney_list = pm.get_tourney_list(tourney_list_id)
    tourney_list.archtype = archtype
    tourney_list.archtype_id = archtype.id
    pm.db_connector.get_session().add(tourney_list)
    pm.db_connector.get_session().commit()

    return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list.id)


@app.route("/generate_hash_keys")
def generate_hash_keys():
    pm = PersistenceManager(myapp.db_connector)
    archtypes = pm.get_all_archtypes()
    for archtype in archtypes:
        if len(archtype.ships) > 0:
            hashkey = archtype.generate_hash_key(archtype.ships)
            archtype.hashkey = hashkey
    pm.db_connector.get_session().commit()
    return redirect(url_for('tourneys'))


@app.route('/display_list')
def display_list():
    tourney_list_id = request.args.get('tourney_list_id')
    admin = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    m = xwingmetadata.XWingMetaData()
    image_src = None
    if tourney_list.image is not None:
        image_src = urllib.quote(tourney_list.image)
    else:
        rand = randint(1, 18)
        image_src = url_for('static', filename="img/" + str(rand) + ".jpg")

    return render_template('list_display.html',
                           meta=m,
                           admin=admin,
                           image_src=image_src,
                           tourney_list=tourney_list,
                           tourney=tourney_list.tourney,
                           tourney_list_id=tourney_list.id,
                           tourney_id=tourney_list.tourney.id)


@app.route("/pretty_print")
def pretty_print():
    pm = PersistenceManager(myapp.db_connector)
    archtypes = pm.get_all_archtypes()
    i = 0
    for a in archtypes:
        if a.pretty is None:
            pp = a.pretty_print_list()
            a.pretty = pp
            pm.db_connector.get_session().add(a)
        i = i + 1
        if i % 1000 == 0:
            print("pretty_printed %d archtypes" % (i))
            pm.db_connector.get_session().commit()
    pm.db_connector.get_session().commit()
    return redirect(url_for('tourneys'))


@app.route("/time_series")
def time_series():
    venue_id = request.args.get('venue_id')
    pm = PersistenceManager(myapp.db_connector)
    pcd = ShipPilotTimeSeriesData(pm,
                                  venue_id=venue_id,
                                  calculate_upgrades=True)
    venue_name = ""
    if venue_id is not None:
        venue = pm.get_venue_by_id(venue_id)
        venue_name = venue.get_name()

    total_options = ShipTotalHighchartOptions(pcd)
    faction_options = FactionTotalHighChartOptions(pcd)

    ships_by_faction = pm.get_ships_by_faction()
    ship_options = ShipHighchartOptions(pcd, ships_by_faction)

    pilots_by_faction = pm.get_pilots_by_faction()
    pilot_options = PilotHighchartOptions(pcd, pilots_by_faction)

    upgrade_options = UpgradeHighChartOptions(pcd)

    tourney_types = pm.get_tourney_types()

    tt = []
    for tourney_type in tourney_types:
        tt.append(tourney_type[0])

    pskill = PilotSkillTimeSeriesData(pm, venue_id)
    pskillgraph = PilotSkillHighchartsGraph(pskill)

    if venue_id is None:
        venue_id = 0
    return render_template("time_series.html",
                           ship_total_options=total_options.options,
                           faction_options=faction_options.options,
                           ship_options=ship_options.options,
                           pilot_options=json.dumps(pilot_options.options),
                           upgrade_options=upgrade_options.options,
                           upgrade_types=sorted(pcd.upgrade_types.keys()),
                           upgrade_name_to_type=pcd.upgrade_name_to_type,
                           pilot_skill_options=pskillgraph.options,
                           tourney_types=tt,
                           ps_ships=sorted(pskill.ships.keys()),
                           scum=Faction.SCUM.description,
                           rebel=Faction.REBEL.description,
                           imperial=Faction.IMPERIAL.description,
                           venue_id=str(venue_id),
                           venue_name=venue_name)


@app.route("/get_ps_time_series", methods=['POST'])
def get_ps_time_series():
    data = request.json['data']
    show_as_percentage = data['show_ps_as_percentage']
    tourney_filters = data['tourney_filters']
    results_type = data['results_type']
    ships = data['ships_filter']
    imperial_checked = data['imperial_checked']
    rebel_checked = data['rebel_checked']
    scum_checked = data['scum_checked']
    venue_id = data['venue_id']

    show_as_count = True

    show_only_the_cut = False
    if results_type is not None and results_type == "cut":
        show_only_the_cut = True

    pm = PersistenceManager(myapp.db_connector)

    pskill = PilotSkillTimeSeriesData(pm,
                                      venue_id=venue_id,
                                      tourney_filters=tourney_filters,
                                      show_the_cut_only=show_only_the_cut)
    pskillgraph = PilotSkillHighchartsGraph(pskill,
                                            ships_filter=ships,
                                            show_as_percentage=show_as_percentage,
                                            rebel_checked=rebel_checked,
                                            scum_checked=scum_checked,
                                            imperial_checked=imperial_checked)
    return jsonify(ps_options=pskillgraph.options)


@app.route("/get_total_time_series", methods=['POST'])
def get_total_time_series():
    data = request.json['data']
    aggregation_type = data['aggregation_type']
    results_type = data['results_type']
    tourney_filters = data['tourney_filters']
    venue_id = data['venue_id']

    show_as_count = True
    if aggregation_type is not None and aggregation_type == "sum":
        show_as_count = False

    show_only_the_cut = False
    if results_type is not None and results_type == "cut":
        show_only_the_cut = True

    pm = PersistenceManager(myapp.db_connector)
    pcd = ShipPilotTimeSeriesData(pm, tourney_filters=tourney_filters,
                                  show_as_count=show_as_count,
                                  show_the_cut_only=show_only_the_cut,
                                  venue_id=venue_id)
    total_options = ShipTotalHighchartOptions(pcd,
                                              show_as_count=show_as_count)
    return jsonify(options=total_options.options)


@app.route("/get_faction_time_series", methods=['POST'])
def get_faction_time_series():
    data = request.json['data']
    show_as_percentage = data['show_faction_as_percentage']
    aggregation_type = data['aggregation_type']
    tourney_filters = data['tourney_filters']
    results_type = data['results_type']
    venue_id = data['venue_id']

    show_as_count = True
    if aggregation_type is not None and aggregation_type == "sum":
        show_as_count = False

    show_only_the_cut = False
    if results_type is not None and results_type == "cut":
        show_only_the_cut = True

    pm = PersistenceManager(myapp.db_connector)
    pcd = ShipPilotTimeSeriesData(pm,
                                  venue_id=venue_id,
                                  tourney_filters=tourney_filters,
                                  show_as_count=show_as_count,
                                  show_the_cut_only=show_only_the_cut)
    faction_options = FactionTotalHighChartOptions(pcd, show_as_percentage, show_as_count)
    return jsonify(faction_options=faction_options.options)


@app.route("/get_ship_time_series", methods=['POST'])
def get_ship_time_series():
    data = request.json['data']
    show_as_percentage = data['show_ship_as_percentage']
    imperial_checked = data['imperial_checked']
    rebel_checked = data['rebel_checked']
    scum_checked = data['scum_checked']
    aggregation_type = data['aggregation_type']
    tourney_filters = data['tourney_filters']
    results_type = data['results_type']
    venue_id = data['venue_id']

    show_as_count = True
    if aggregation_type is not None and aggregation_type == "sum":
        show_as_count = False

    show_only_the_cut = False
    if results_type is not None and results_type == "cut":
        show_only_the_cut = True

    pm = PersistenceManager(myapp.db_connector)
    pcd = ShipPilotTimeSeriesData(pm,
                                  venue_id=venue_id,
                                  tourney_filters=tourney_filters,
                                  show_as_count=show_as_count,
                                  show_the_cut_only=show_only_the_cut)
    ships_by_faction = pm.get_ships_by_faction()
    ship_options = ShipHighchartOptions(pcd,
                                        ships_by_faction,
                                        show_as_count=show_as_count,
                                        show_as_percentage=show_as_percentage,
                                        rebel_checked=rebel_checked,
                                        scum_checked=scum_checked,
                                        imperial_checked=imperial_checked,
                                        top_10_only=False)
    return jsonify(ship_options=ship_options.options)


@app.route("/get_pilot_time_series", methods=['POST'])
def get_pilot_time_series():
    data = request.json['data']
    show_as_percentage = data['show_pilot_as_percentage']
    imperial_checked = data['imperial_checked']
    rebel_checked = data['rebel_checked']
    scum_checked = data['scum_checked']
    aggregation_type = data['aggregation_type']
    tourney_filters = data['tourney_filters']
    results_type = data['results_type']
    venue_id = data['venue_id']

    show_as_count = True
    if aggregation_type is not None and aggregation_type == "sum":
        show_as_count = False

    show_only_the_cut = False
    if results_type is not None and results_type == "cut":
        show_only_the_cut = True

    pm = PersistenceManager(myapp.db_connector)
    pcd = ShipPilotTimeSeriesData(pm,
                                  venue_id=venue_id,
                                  tourney_filters=tourney_filters,
                                  show_as_count=show_as_count,
                                  show_the_cut_only=show_only_the_cut)
    pilots_by_faction = pm.get_pilots_by_faction()
    pilot_options = PilotHighchartOptions(pcd,
                                          pilots_by_faction,
                                          show_as_count=show_as_count,
                                          show_as_percentage=show_as_percentage,
                                          rebel_checked=rebel_checked,
                                          scum_checked=scum_checked,
                                          imperial_checked=imperial_checked,
                                          top_10_only=False)
    return jsonify(pilot_options=pilot_options.options)


@app.route("/get_upgrade_time_series", methods=['POST'])
def get_upgrade_time_series():
    data = request.json['data']
    show_as_percentage = data['show_upgrade_as_percentage']
    aggregation_type = data['aggregation_type']
    tourney_filters = data['tourney_filters']
    results_type = data['results_type']
    venue_id = data['venue_id']

    show_as_count = True
    if aggregation_type is not None and aggregation_type == "sum":
        show_as_count = False

    show_only_the_cut = False
    if results_type is not None and results_type == "cut":
        show_only_the_cut = True

    pm = PersistenceManager(myapp.db_connector)
    pcd = ShipPilotTimeSeriesData(pm,
                                  venue_id=venue_id,
                                  tourney_filters=tourney_filters,
                                  show_as_count=show_as_count,
                                  show_the_cut_only=show_only_the_cut,
                                  calculate_ship_pilot=False,
                                  calculate_upgrades=True)
    upgrade_options = UpgradeHighChartOptions(pcd,
                                              show_as_count=show_as_count,
                                              show_as_percentage=show_as_percentage,
                                              top_10_only=False)
    return jsonify(upgrade_options=upgrade_options.options)


@app.route("/fix_venue_dupes")
def fix_venue_dupes():
    pm = PersistenceManager(myapp.db_connector)
    venues = pm.get_venues()
    fixes = {}
    for v in venues:
        key = "%s-%s-%s-%s" % (v.country, v.state, v.city, v.venue)
        if not fixes.has_key(key):
            fixes[key] = {'first': v, 'goners': []}
        else:
            fixes[key]['goners'].append(v)

    goners = []
    for href in fixes.values():
        first = href['first']
        g = href['goners']
        for goner in g:
            adjusted_tourneys = goner.tourneys
            for adjusted_tourney in adjusted_tourneys:
                adjusted_tourney.venue = first
            goners.append(goner)
    pm.db_connector.get_session().commit()

    # print("deleting %d venues" % ( len( goners )))

    for goner in goners:
        pm.db_connector.get_session().delete(goner)

    pm.db_connector.get_session().commit()

    return redirect(url_for("tourneys"))


@app.route("/set_geo")
def set_geo():
    pm = PersistenceManager(myapp.db_connector)
    venues = pm.get_venues()
    g = Nominatim()
    data = {}
    seen = {}
    i = 0
    for venue in venues:
        city = venue.get_city()
        state = venue.get_state()
        country = venue.get_country()
        key = "%s %s %s" % (city, state, country)
        l = None
        if not seen.has_key(key):
            try:
                print "looking up key %s for venue %d" % (key, venue.id)
                l = g.geocode(key)
            except:
                print "unable to lookup key %s" % (key)
            seen[key] = l
        else:
            l = seen[key]
        if not l:
            continue
        venue.latitude = l.latitude
        venue.longitude = l.longitude

        if i % 10 == 0:
            print "processed %d records" % (i)
        i += 1

    pm.db_connector.get_session().commit()
    return redirect(url_for("venues"))


@app.route("/venue")
def venue():
    pm = PersistenceManager(myapp.db_connector)
    venue_id = request.args.get('venue_id')
    venue = pm.get_venue_by_id(venue_id)
    return render_template('venue.html', venue=venue)


@app.route("/heatmap")
def heatmap():
    pm = PersistenceManager(myapp.db_connector)
    venues = pm.get_venues()
    data = []
    for venue in venues:
        if venue.latitude is not None and venue.longitude is not None:
            markup = Markup("%s: %d event(s)" % (venue.venue_url(), len(venue.tourneys)))
            data.append({'count': len(venue.tourneys),
                         'lat': float(venue.latitude),
                         'lng': float(venue.longitude),
                         'name': str(markup.decode()),

                         }
                        )

    return render_template("heat_map.html", data=data, venues=venues)


@app.route("/edit_venue_geo", methods=['POST'])
def edit_venue_geo():
    pm = PersistenceManager(myapp.db_connector)
    venue_id = request.values['data[id]']
    lat = request.values['data[lat]']
    lng = request.values['data[lng]']
    name = request.values['data[name]']
    num_events = request.values['data[num_events]']
    city = request.values['data[city]']
    state = request.values['data[state]']
    country = request.values['data[country]']

    venue = pm.get_venue_by_id(venue_id)

    venue.longitude = lng
    venue.latitude = lat
    venue.venue = name
    venue.city = city
    venue.state = state
    venue.country = country

    pm.db_connector.get_session().commit()

    return json.dumps({"row": {'id': venue_id,
                               'name': name,
                               'lat': lat,
                               'lng': lng,
                               'num_events': num_events,
                               'city': city,
                               'state': state,
                               'country': country}})


def to_float(dec):
    return float("{0:.2f}".format(float(dec) * float(100)))

@app.route("/label_data")
def label_data():
    xwing_data = simple_cache.get('xwing-data')
    if xwing_data is None:
        xwing_data = {}
        #pm = PersistenceManager(myapp.db_connector)
        dir = os.path.join(static_root, "xwing-data")
        ships_file = os.path.join(dir, "ships.js")
        with open(ships_file) as data_file:
            ships_data = json.loads(data_file.read())
            xwing_data['ships'] = ships_data
        source_file = os.path.join(dir, "sources.js")
        with open(source_file) as data_file:
            sources_data = json.loads(data_file.read())
            xwing_data['sources'] = ships_data
        upgrade_file = os.path.join(dir, 'upgrades.js')
        with open(upgrade_file) as data_file:
            upgrade_data = json.loads(data_file.read())
            xwing_data['upgrades'] = upgrade_data
        simple_cache.set('xwing-data', xwing_data)

        ship_map= {}
        upgrade_map = {}
        for sd in sources_data:
            wave = sd['wave']
            ships = sd['contents']['ships']
            upgrades = sd['contents']['upgrades']
            for xwing_data_ship_id in ships:
                if not ship_map.has_key(xwing_data_ship_id):
                    ship_map[xwing_data_ship_id] = { 'xwing_data_id': xwing_data_ship_id,
                                                     'wave':wave,
                                                     'xws': None}
            for xwing_data_upgrade_id in upgrades:
                if not upgrade_map.has_key(xwing_data_upgrade_id):
                    upgrade_map[xwing_data_upgrade_id] = {'xwing_data_id': xwing_data_upgrade_id, 'wave':wave, 'xws':None}

        for ship in ships_data:
            sm = ship_map[str(ship['id'])]
            sm['xws'] = ship['xws']

        for upgrade in upgrade_data:
            um = upgrade_map[str(upgrade['id'])]
            if um['wave'] in (0,1):
                um['xws'] = upgrade['xws']

        wave_one_ships    = [s['xws'] for s in ship_map.values() if s['wave'] in (0,1)]
        wave_one_upgrades = {}
        for u in upgrade_map.values():
            if not wave_one_upgrades.has_key(u['xws']):
                wave_one_upgrades[u['xws']] = 1
        pm = PersistenceManager(myapp.db_connector)
        wave_one_lists = pm.get_wave_one_lists(wave_one_ships,wave_one_upgrades)
        xwing_data['wave_one_lists'] = wave_one_lists


    return render_template("label_data.html", lists=xwing_data['wave_one_lists'] )



@app.route("/merge_tourney_lists")
def merge_tourney_lists():
    from_tourney_id = request.args.get('from_tourney_id')
    to_tourney_id = request.args.get('to_tourney_id')

    pm = PersistenceManager(myapp.db_connector)
    from_tourney = pm.get_tourney_by_id(from_tourney_id)
    to_tourney   = pm.get_tourney_by_id(to_tourney_id)

    #collect all the lists in the from tourney
    list_map = {}
    for list in from_tourney.tourney_lists:
        if list.archtype_list is not None:
            list_map[list.player.get_player_name()] = list

    #and merge them into the to tourney
    for to_list in to_tourney.tourney_lists:
        #see if its in the map
        if to_list.player.get_player_name() in list_map:
            from_list = list_map[to_list.player.get_player_name()]
            to_list.archtype_id = from_list.archtype_id

    pm.db_connector.get_session().commit()
    return redirect(url_for("get_tourney_details", tourney_id=to_tourney.id))

@app.route("/auto_lock_tourneys")
def auto_lock_tourneys():
    pm = PersistenceManager(myapp.db_connector)
    tourneys = pm.get_tourneys()
    time_threshold = datetime.today() - timedelta(days=1 * 365 / 12)
    time_threshold = time_threshold.date()

    for tourney in tourneys:
        tourney_date = tourney.tourney_date
        if tourney_date and tourney_date < time_threshold:
            tourney.locked = 1
    pm.db_connector.get_session().commit()
    return redirect(url_for("tourneys"))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'dev':
            app.debug = True
        else:
            app.debug = False
    else:
        app.debug = False
    app.run(port=5002)
