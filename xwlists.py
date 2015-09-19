import json
import os
from random import randint
import urllib
import datetime
import uuid
from flask import render_template, request, url_for, redirect, jsonify, Response, send_from_directory
from flask.ext.mail import Mail, Message
import sys
import requests
from sqlalchemy import func
from werkzeug.utils import secure_filename
from api import TournamentsAPI, TournamentAPI, PlayersAPI, PlayerAPI, TournamentSearchAPI, TournamentTokenAPI

from cryodex import Cryodex
from dataeditor import RankingEditor, RoundResultsEditor
from decoder import decode
import myapp
from persistence import Tourney, TourneyList, PersistenceManager,  Faction, Ship, ShipUpgrade, UpgradeType, Upgrade, \
    TourneyRound, RoundResult, TourneyPlayer, TourneyRanking, TourneySet, TourneyVenue, Event, ArchtypeList
from rollup import Rollup
from search import Search
from uidgen import ListUIDGen
import xwingmetadata
from xws import VoidStateXWSFetcher, XWSToJuggler, YASBFetcher, FabFetcher
from flask.ext import restful
from flask_cors import CORS

YASB = 'yasb'

VOIDSTATE = "voidstate"

app =  myapp.create_app()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
UPLOAD_FOLDER = "static/tourneys"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set( ['png', 'jpg', 'jpeg', 'gif', 'html', 'json'])

is_maintenance_mode = False

here = os.path.dirname(__file__)
static_dir = os.path.join( here, app.config['UPLOAD_FOLDER'] )


MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

from werkzeug.contrib.cache import SimpleCache
simple_cache = SimpleCache()


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD
))

# administrator list
ADMINS = ['sozinsky@gmail.com']

mail = Mail(app)

session = myapp.db_connector.get_session()


api = restful.Api(app)
api.add_resource(TournamentsAPI, '/api/v1/tournaments')
api.add_resource(TournamentAPI, '/api/v1/tournament/<int:tourney_id>' )
api.add_resource(PlayersAPI, '/api/v1/tournament/<int:tourney_id>/players' )
api.add_resource(PlayerAPI, '/api/v1/tournament/<int:tourney_id>/player/<int:player_id>' )

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
        print("sending msg ")
        mail.send(msg)


def mail_error(errortext):
    msg = Message('XWJuggler Error', sender=ADMINS[0], recipients=ADMINS)
    msg.body = 'text body'
    msg.html = '<b>ERROR</b><br><hr>' + errortext
    with app.app_context():
        print("sending msg ")
        mail.send(msg)


#@app.before_request
#def check_for_maintenance():
#    return render_template('maintenance.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/search")
def versus():
    return render_template("search.html")


@app.route("/search_guide")
def search_guide():
    return render_template("search_guide.html")


@app.route("/search_results", methods=['POST'])
def get_search_results():
    try:
        search_text = request.json['search-text']
        s = Search( search_text )
        results = s.search()
        return render_template( 'search_results.html', results=results), 200
    except ValueError, e:
        return render_template( 'search_error.html', errortext=str(e))



@app.route("/events")
def events():
    events = PersistenceManager(myapp.db_connector).get_events()
    return render_template("event.html", events=events)

@app.route( "/tourney_admin")
def tourney_admin():
    tourneys = PersistenceManager(myapp.db_connector).get_tourneys()
    return render_template("tourney_admin.html", tourneys=tourneys)

@app.route("/tourneys")
def tourneys():
    admin_on = request.args.get('admin')
    if admin_on is not None:
        admin_on = True
    else:
        admin_on = False
    tourneys = PersistenceManager(myapp.db_connector).get_tourneys()
    return render_template('tourneys.html', tourneys=tourneys, admin=admin_on )

@app.route("/tourney_results")
def get_tourney_results():
    tourney_id   = request.args.get('tourney_id')
    return redirect(url_for('get_tourney_details', tourney_id=tourney_id))

@app.route('/show_results')
def show_results():
    hashkey = request.args.get('hashkey')
    pm   = PersistenceManager(myapp.db_connector)
    lists = pm.get_lists_for_hashkey(hashkey)
    results = []
    ret     = {}
    ret[ 'pretty_print'] = lists[0][0].pretty_print( manage_list=0, show_results=0)
    ret['hashkey'] = lists[0][1].hashkey
    for listpair in lists:
        list = listpair[0]
        res = pm.get_round_results_for_list(list.id)
        for r in res:
            results.append(r)
    ret[ "results"] = results
    return render_template("show_results.html", data=ret)



@app.route("/correct_list_points")
def correct_list_points():

    pm                = PersistenceManager(myapp.db_connector)
    lists             = pm.get_all_lists()
    for list in lists:
        if list.points() == 0 and len(list.ships()) > 0:
            print "list %d is a problem" % list.id
    return redirect(url_for('tourneys') )

@app.route("/edit_tourney_details")
def edit_tourney_details():
    tourney_id   = request.args.get('tourney_id')

    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)

    tourney_date      = tourney.tourney_date
    date_str          = "%d/%d/%d" % ( tourney_date.month, tourney_date.day, tourney_date.year)
    print "tourney date is " + date_str

    return render_template('edit_tourney_details.html', tourney_id=tourney_id,
                                                tourney=tourney,
                                                tourney_formats = xwingmetadata.formats,
                                                tourney_date = date_str,
                                                unlocked=False )

@app.route("/update_tourney_details/",methods=['POST'])
def update_tourney_details():
    tourney_id            = request.form['tourney_id']
    name                  = decode( request.form['name'] )
    type                  = request.form['tourney_type']
    print request.form['datepicker']
    mmddyyyy              = request.form['datepicker'].split('/')
    date                  = datetime.date( int(mmddyyyy[2]),int(mmddyyyy[0]), int(mmddyyyy[1])) #YYYY, MM, DD
    round_length  = request.form['round_length_userdef']
    tourney_format_def    = request.form['tourney_format_dropdown']
    tourney_format_custom = request.form['tourney_format_custom']
    participant_count     = int(request.form['participant_count'])
    country               = decode(request.form['country'])
    state                 = decode(request.form['state'])
    city                  = decode(request.form['city'])
    venue                 = decode(request.form['venue'])


    tourney_format = None
    if tourney_format_def is None or len(tourney_format_def) == 0:
        if tourney_format_custom is None or len(tourney_format_custom) == 0:
            tourney_format = xwingmetadata.format_default
        else:
            tourney_format = decode(tourney_format_custom)
    else:
        tourney_format = str(tourney_format_def)


    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)

    tourney.tourney_name = name
    tourney.tourney_type  = type
    tourney.tourney_date = date
    tourney.round_length = round_length
    tourney.format = tourney_format
    tourney.participant_count = participant_count
    tourney.venue.country = country
    tourney.venue.state = state
    tourney.venue.city = city
    tourney.venue.venue = venue

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="edit tourney information",
                  event_details="edited " + name )

    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return redirect( url_for( 'get_tourney_details', tourney_id=tourney_id) )



@app.route("/get_tourney_details")
def get_tourney_details():
    tourney_id   = request.args.get('tourney_id')

    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)

    unlocked = True
    if tourney.locked:
        unlocked = False

    return render_template('edit_tourney.html', tourney_id=tourney_id,
                                                tourney=tourney,
                                                unlocked=unlocked )


def create_default_editor_ranking(i, row):
    row['player_id'] = None
    row['player_name'] = 'Player%d' % ( i )
    row['score'] = 0
    row['swiss_rank'] = i
    row['dropped'] = False
    row['championship_rank'] = None
    row['mov'] = 0
    row['sos'] = 0


@app.route("/get_rankings")
def get_tourney_data():
    tourney_id        = request.args['tourney_id']
    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)

    de = RankingEditor( pm, tourney )
    return de.get_json()

@app.route("/get_pre_elim_results")
def get_pre_elim_results():
    tourney_id = request.args['tourney_id']
    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)
    er = RoundResultsEditor(pm, tourney, pre_elim=True)
    json_ret = er.get_json()
    return json_ret

@app.route("/get_elim_results")
def get_elim_results():
    tourney_id = request.args['tourney_id']
    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)
    er = RoundResultsEditor(pm, tourney, pre_elim=False)
    json_ret = er.get_json()
    return json_ret

@app.route("/edit_rankings",methods=['POST'])
def edit_ranking_row():

    #see https://editor.datatables.net/manual/server
    tourney_id        = request.args['tourney_id']
    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)

    de = RankingEditor(pm, tourney)

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


def edit_results( request, pre_elim=True):
    #see https://editor.datatables.net/manual/server
    tourney_id        = request.args['tourney_id']
    pm                = PersistenceManager(myapp.db_connector)
    tourney           = pm.get_tourney_by_id(tourney_id)

    rre = RoundResultsEditor(pm, tourney, pre_elim)
    ret = rre.get_and_set_json( request )
    return ret

@app.route("/edit_pre_elim_results", methods=['POST'])
def edit_pre_elim_results():
    return edit_results( request, True )

@app.route("/edit_elim_results", methods=['POST'])
def edit_elim_results():
    #see https://editor.datatables.net/manual/server
    return edit_results( request, True )


@app.route("/new")
def new():
    set = sorted(xwingmetadata.sets_and_expansions.keys() )
    return render_template('new_tourney.html', sets      = set,
                                               tourney_formats = xwingmetadata.formats,
                                               format_default  = xwingmetadata.format_default )

def generate( rows ):
    for r in rows:
        yield ",".join(r) + "\n"

def get_tourney_lists_as_text(tourney, make_header=True ):

    rows   = []
    header =  xwingmetadata.header()

    if make_header:
        rows.append( header )

    tourney_date = "%d/%d/%d" % ( tourney.tourney_date.month, tourney.tourney_date.day, tourney.tourney_date.year )
    row_defaults = [ tourney.tourney_name.replace(',',' '), tourney.tourney_type, tourney_date ]

    for tourney_list in tourney.tourney_lists:
        if tourney_list.ships() is None or len(tourney_list.ships()) == 0:
            new_row = []
            new_row.extend ( row_defaults )
            for i in range (len(new_row), len(header)):
                new_row.append('')
            rows.append(new_row)
        else:
            for ship in tourney_list.ships():
                new_row = []
                new_row.extend( row_defaults )
                new_row.extend( [ tourney_list.player.player_name.replace(',',' '),
                                  tourney_list.faction().description,
                                  str(tourney_list.points()),
                                  str(tourney_list.player.result.rank),
                                  str(tourney_list.player.result.elim_rank),
                                  str(tourney_list.id),
                                  ship.ship_pilot.ship_type.description,
                                  ship.ship_pilot.pilot.name
                ] )

                for i in range(len(new_row), len(header)):
                    new_row.append( ship.get_upgrade( header[i]  ) )

                rows.append(new_row)
    return rows

def csv_response(rows, name):
    disposition = "attachment; filename=" + name
    return Response(generate(rows), mimetype='text/csv', headers={'Content-Disposition': disposition} )


@app.route("/export_all_lists")
def export_all_lists():
    pm          = PersistenceManager(myapp.db_connector)
    tourneys    = pm.get_tourneys();
    make_header = True
    rows        = []
    for tourney in tourneys:
        ret = get_tourney_lists_as_text(tourney, make_header)
        make_header = False
        rows.extend( ret )

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="export all tourney lists")
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()
    return csv_response( rows, "all_lists_download.csv")


@app.route("/export_tourney_lists")
def export_tourney_lists():
    tourney_id = request.args.get('tourney_id')
    pm         = PersistenceManager(myapp.db_connector)
    tourney    = pm.get_tourney_by_id(tourney_id)

    ret = get_tourney_lists_as_text(tourney)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="export tourney lists",
                  event_details="exported tourney %s" % ( tourney.tourney_name ))
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return csv_response( ret, "tourney_list_download.csv")


@app.route("/delete_tourney")
def delete_tourney():
    tourney_name = request.args.get('tourney')
    pm = PersistenceManager(myapp.db_connector)
    pm.delete_tourney(tourney_name)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="delete tourney",
                  event_details="deleted tourney %s" % ( tourney_name ))
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return redirect(url_for('tourneys') )


def add_sets_and_venue_to_tourney(city, country, pm, sets_used, state, t, venue):
    #load in the sets used
    if sets_used:
        for set_name in sets_used:
            set = pm.get_set(set_name)
            if set is not None:
                ts = TourneySet(tourney=t, set=set)
                pm.db_connector.get_session().add(ts)
    tv = TourneyVenue(tourney=t, country=country, state=state, city=city, venue=venue)
    t.venue = tv
    pm.db_connector.get_session().add(tv)


def create_tourney(cryodex, tourney_name, tourney_date, tourney_type,
                   round_length, sets_used, country, state, city, venue, email, participant_count, tourney_format):

    pm = PersistenceManager(myapp.db_connector)
    t = Tourney(tourney_name=tourney_name, tourney_date=tourney_date,
                tourney_type=tourney_type, round_length=round_length, email=email, entry_date=datetime.datetime.now(),
                participant_count=participant_count, locked=False, format=tourney_format)

    pm.db_connector.get_session().add(t)
    #add the players
    players = {}
    lists  = {}

    for player in cryodex.players.keys():
        tp = TourneyPlayer( tourney=t, player_name=player)
        tlist = TourneyList(tourney=t, player=tp)
        pm.db_connector.get_session().add(tlist)
        players[player] = tp
        lists[player]   = tlist


    pm.db_connector.get_session().commit()

    for round_type in cryodex.rounds.keys():
        rounds = cryodex.rounds[round_type]
        for round in rounds:
            tr = TourneyRound(round_num=int(round.number), round_type=round.get_round_type(), tourney=t)
            pm.db_connector.get_session().add(tr)
            for round_result in round.results:
                rr = None
                if round_result.bye:
                    p1_tourney_list = lists[ round_result.player1 ]
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
                                     list2_score=round_result.player2_score, bye=round_result.bye, draw=round_result.draw)
                pm.db_connector.get_session().add(rr)

    add_sets_and_venue_to_tourney(city, country, pm, sets_used, state, t, venue)

    #finally load the rankings
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
            #cryodex provided a list id ... load it
            try:
                tourney_list = lists[rank.player_name]
                fetcher = VoidStateXWSFetcher()
                xws = fetcher.fetch(rank.list_id)
                converter = XWSToJuggler(xws)
                converter.convert(pm, tourney_list)

            except Exception as err:
                print ("unable to fetch list id " + rank.list_id + " from voidstate, reason: " + str(err) )
                mail_error(errortext=str(err) + "<br><br>Unable to fetch list id " + rank.list_id + " from voidstate" )



    #and commit all the work
    pm.db_connector.get_session().commit()
    return t

def save_cryodex_file( failed, filename, data ):
    dir = None
    if failed:
        dir = os.path.join( static_dir, "cryodex/fail")
    else:
        dir = os.path.join( static_dir, "cryodex/success")
    file = os.path.join( dir, filename )
    fd = open( file, 'w' )
    fd.write( data.encode('utf8') )
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
                    rec = { 'tourney' : decode(tourney.tourney_name),
                            'num_participants': tourney.participant_count,
                            'player' : decode(rank.player.player_name),
                            'swiss_standing': rank.rank,
                            'championship_standing' : rank.elim_rank,
                            'pretty_print' : rank.pretty_print() }
                    store_champs.append(rec)

        simple_cache.set( 'store-champ-data', store_champs, timeout=5*60)

    return render_template( 'store_champ_lists.html', championship_lists=store_champs)


@app.route("/add_tourney",methods=['POST'])
def add_tourney():

    #TODO: better edge testing against user input
    name                  = decode( request.form['name'] )
    email                 = decode( request.form['email'] )
    type                  = request.form['tourney_type']
    mmddyyyy              = request.form['datepicker'].split('/')
    date                  = datetime.date( int(mmddyyyy[2]),int(mmddyyyy[0]), int(mmddyyyy[1])) #YYYY, MM, DD
    round_length_dropdown = request.form['round_length_dropdown']
    round_length_userdef  = request.form['round_length_userdef']
    tourney_format_def    = request.form['tourney_format_dropdown']
    tourney_format_custom = request.form['tourney_format_custom']
    participant_count     = int(request.form['participant_count'])
    sets_used             = request.form.getlist('sets[]')
    country               = decode(request.form['country'])
    state                 = decode(request.form['state'])
    city                  = decode(request.form['city'])
    venue                 = decode(request.form['venue'])

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

    tourney_report  = request.files['tourney_report']

    mail_message("New tourney creation attempt", "Request to create tourney name %s from user %s of type %s on day %s with %d participants" % \
          ( name, email, type, date, participant_count) )

    if tourney_report:
        filename        = tourney_report.filename
        data            = None
        if tourney_report and allowed_file(filename):
            try:
                data = tourney_report.read()
                data = decode(data)
                cryodex = Cryodex(data, filename)
                t = create_tourney(cryodex, name, date, type, round_length,
                                   sets_used, country, state, city, venue, email, participant_count, tourney_format )
                sfilename = secure_filename(filename) + "." + str(t.id)
                save_cryodex_file( failed=False, filename=sfilename, data=data)

                event = Event(remote_address=myapp.remote_address(request),
                              event_date=func.now(),
                              event="create tourney",
                              event_details="created tourney %s from croydex input" % ( t.tourney_name ))
                pm = PersistenceManager(myapp.db_connector)
                pm.db_connector.get_session().add(event)
                pm.db_connector.get_session().commit()
                mail_message("New cryodex tourney created", "A new tourney named '%s' with id %d was created from file %s!" % ( t.tourney_name, t.id, filename ))
                print "getting tourney details"
                return redirect( url_for('get_tourney_details', tourney_id=t.id))
            except (Exception,UnicodeEncodeError ) as err:
                filename=str(uuid.uuid4()) + ".html"
                save_cryodex_file( failed=True, filename=filename, data=data)
                mail_error(errortext=str(err) + "<br><br>Filename =" + filename )
                return render_template( 'tourney_entry_error.html', errortext=str(err))


    else: #user didnt provide a cryodex file ... have to do it manually
        try:
            pm = PersistenceManager(myapp.db_connector)
            t = Tourney(tourney_name=name, tourney_date=date, tourney_type=type, locked=False,
                        round_length=round_length, email=email, entry_date=datetime.datetime.now(),
                        participant_count=participant_count,format=tourney_format)
            pm.db_connector.get_session().add(t)
            add_sets_and_venue_to_tourney(city, country, pm, sets_used, state, t, venue )
            pm.db_connector.get_session().commit()
            event = Event(remote_address=myapp.remote_address(request),
                          event_date=func.now(),
                          event="create tourney",
                          event_details="created tourney %s from manual input" % ( t.tourney_name ))
            pm = PersistenceManager(myapp.db_connector)
            pm.db_connector.get_session().add(event)
            pm.db_connector.get_session().commit()
            mail_message("New manual tourney created", "A new tourney named '%s' with id %d was created!" % ( t.tourney_name, t.id ))
            return redirect(url_for('get_tourney_details', tourney_id=t.id))
        except Exception as err:
            mail_error(errortext=str(err))
            return render_template( 'tourney_entry_error.html', errortext=str(err))



    #TODO: this is code for handling the scanned player list scenario.   I'll refactor it to something useful if the situation comes up again.
    #load all the files in the folder
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

    #myapp.db_connector.get_session().add_all( lists )
    #myapp.db_connector.get_session().commit()

@app.route("/browse_list")
def browse_list():
    tourney_name = request.args.get('tourney')
    admin        = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney(tourney_name)
    tourney_lists = tourney.tourney_lists
    return render_template( 'tourney_lists.html', tourney=tourney, tourney_lists=tourney_lists, admin=admin)

#WTF googlebot?
@app.route("/delete_list_and_retry_list_entry")
def delete_list_and_retry():
    tourney_list_id = request.args.get('tourney_list_id')
    print("calling delete list and retry on tourney id " + tourney_list_id)

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    pm.delete_tourney_list_details( tourney_list )

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="delete list",
                  event_details="deleted list id %d from tourney %s" % ( tourney_list.id, tourney_list.tourney.tourney_name ))
    pm = PersistenceManager(myapp.db_connector)
    pm.db_connector.get_session().add(event)
    pm.db_connector.get_session().commit()

    return redirect( url_for('enter_list', tourney=tourney_list.tourney.id, tourney_list_id=tourney_list.id ) )

@app.route( "/success")
def success():
    tourney_name = request.args.get("tourney_name")
    return render_template( "success_kid.html", tourney_name=tourney_name)


@app.route("/enter_list")
def enter_list():
    tourney_id    = request.args.get('tourney')
    tourney_list_id = request.args.get('tourney_list_id')

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = None
    tourney = None

    if tourney_list_id is None:
        tourney = pm.get_tourney_by_id(tourney_id)
        tourney_list = pm.get_random_tourney_list(tourney)
        if tourney_list is None:
            return redirect(url_for( "success", tourney_name=tourney.tourney_name ) )
    else:
        tourney_list = pm.get_tourney_list(tourney_list_id)
        tourney      = tourney_list.tourney

    m = xwingmetadata.XWingMetaData()

    image_src = None
    if tourney_list.image is not None:
        image_src = urllib.quote(tourney_list.image)

    event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="create list",
                  event_details="created list %d for tourney %s" % ( tourney_list.id,  tourney.tourney_name ))
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
            simple_cache.set( 'banner-summary-data', summaries, timeout=5*60)
        return json.dumps( summaries  )
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
        xws     = fetcher.fetch( fab )
        converter = XWSToJuggler(xws)
        converter.convert( pm, tourney_list )
        pm.db_connector.get_session().commit()
        return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list_id)
    except Exception, e:
         mail_error( "Unable to fetch from fab for url " + fab + ", reason: " + str(e))
         response = jsonify(message=str(e))
         response.status_code = (500)
         return response


@app.route("/mysql")
def mysql():
    print "trying to fetch prod.sql from mysqldb endpoint"
    return url_for( 'static', filename='prod.sql')

@app.route("/get_from_yasb", methods=['POST'])
def get_from_yasb():
    try:
        yasb = request.args.get('yasb')
        tourney_id = request.args.get('tourney_id')
        tourney_list_id = request.args.get('tourney_list_id')
        pm = PersistenceManager(myapp.db_connector)
        tourney_list = pm.get_tourney_list(tourney_list_id)

        fetcher = YASBFetcher()
        xws     = fetcher.fetch( yasb )
        converter = XWSToJuggler(xws)
        converter.convert( pm, tourney_list )

        pm.db_connector.get_session().commit()
        return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list_id)
    except Exception, e:
         mail_error( "Unable to fetch from yasb for id " + yasb + ", reason: " + str(e))
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
         converter.convert( pm, tourney_list )
         pm.db_connector.get_session().commit()
         return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list.id)
     except Exception, e:
         mail_error( "Unable to fetch from voidstate for id " + voidstate_id + ", reason: " + str(e))
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
            response = jsonify( result="success")
            if tourney.locked == True: #flip the lock
                tourney.locked = False
                state = "unlocked"
            else:
                tourney.locked = True
                state = "locked"
            event = Event(remote_address=myapp.remote_address(request),
                  event_date=func.now(),
                  event="lock/unlock tourney",
                  event_details="set tourney %s to state %s" % ( tourney.tourney_name, state ))
            pm.db_connector.get_session().add(event)
            pm.db_connector.get_session().commit()
            return response
        else:
            response = jsonify(result="fail")
            return response
    except Exception, e:
        error = "someone tried to unlock tourney_id " + tourney_id + " with email address " + key + " ( expected " + tourney.email + " ) "
        mail_error( error  )
        response = jsonify(message=str(e))
        response.status_code = (500)
        return response

@app.route("/add_squad",methods=['POST'])
def add_squad():
         data         = request.json['data']
         points       = request.json['points']
         faction      = request.json['faction']

         tourney_id = request.args.get('tourney_id')
         tourney_list_id = request.args.get('tourney_list_id')

         pm = PersistenceManager(myapp.db_connector)

         #if an existing archtype already exists, use it it
         #otherwise create a new archtype

         ships = []
         for squad_member in data:
             ship_pilot = pm.get_ship_pilot( squad_member['ship'], squad_member['pilot'] )
             ship       = Ship( ship_pilot_id=ship_pilot.id, ship_pilot=ship_pilot )
             for upgrade in squad_member['upgrades']:
                 upgrade = pm.get_upgrade(upgrade['type'], upgrade['name'])
                 ship_upgrade = ShipUpgrade( ship_id=ship.id,
                                             upgrade=upgrade )
                 ship.upgrades.append( ship_upgrade )
             ships.append( ship )

         hashkey = ArchtypeList.generate_hash_key(ships)

         archtype = pm.get_archtype(hashkey)

         if archtype is None:
             #ding ding!
             #we've never seen this list before!
             archtype = ArchtypeList()
             pm.db_connector.get_session().add(archtype)
             archtype.ships = ships
             for ship in ships:
                 ship.archtype = archtype
                 pm.db_connector.get_session().add(ship)
             archtype.faction = Faction.from_string( faction )
             archtype.points = points
             pm.db_connector.get_session().commit()

         tourney_list = pm.get_tourney_list(tourney_list_id)
         tourney_list.archtype = archtype
         tourney_list.archtype_id = archtype.id
         pm.db_connector.get_session().add(tourney_list)
         pm.db_connector.get_session().commit()

         return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list.id)


@app.route( "/listrank")
def list_rank():
    return render_template("listrank.html")

@app.route("/listrank_generate_cache", methods=['POST'])
def list_rank_generate_cache():

    list_ranks = simple_cache.get('list-ranks')
    if list_ranks is None:
        pm = PersistenceManager(myapp.db_connector)
        list_ranks = pm.get_list_ranks()
        simple_cache.set( 'list-ranks', list_ranks, timeout=60*60)
    return render_template("listrank_impl.html", ranks=list_ranks)

@app.route("/generate_hash_keys")
def generate_hash_keys():
    pm = PersistenceManager( myapp.db_connector )
    gen = ListUIDGen(pm)
    gen.generate()
    return redirect(url_for('tourneys') )

@app.route('/display_list')
def display_list():
    tourney_list_id = request.args.get('tourney_list_id')
    admin           = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    m = xwingmetadata.XWingMetaData()
    image_src = None
    if tourney_list.image is not None:
        image_src=urllib.quote(tourney_list.image)
    else:
        rand = randint(1,18)
        image_src=url_for( 'static', filename="imgs/" + str(rand) + ".jpg")

    return render_template('list_display.html',
                           meta=m,
                           admin=admin,
                           image_src=image_src,
                           tourney_list=tourney_list,
                           tourney=tourney_list.tourney,
                           tourney_list_id=tourney_list.id,
                           tourney_id=tourney_list.tourney.id )

@app.route('/down')
def down():
    return render_template( 'down.html')

@app.route('/')
def index():
    return redirect(url_for('tourneys') )


@app.route("/get_chart_data", methods=['POST'])
def get_chart_data():
    data         = request.json['data']
    rollup       = Rollup( PersistenceManager(myapp.db_connector),
                           data['value'],
                           data['eliminationOnly'],
                           data['storeChampionshipsOnly'],
                           data['regionalChampionshipsOnly'],
                           data['nationalChampionshipsOnly'])
    chart_data   = rollup.rollup()
    return jsonify(data=chart_data,
                   title=data['value'] + rollup.title(),
                   firstCategory=rollup.first_category(),
                   secondCategory=rollup.second_category())


def to_float(dec):
    return float("{0:.2f}".format( float(dec) * float(100)))

@app.route("/tableau")
def tableau():
    return render_template('tableau.html')

@app.route("/charts")
def charts():
    return render_template('charts.html')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'dev':
            app.debug = True
        else:
            app.debug = False
    else:
        app.debug = False
    app.run()
