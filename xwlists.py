import os
import urllib
import datetime

from flask import render_template, request, url_for, redirect, jsonify, Response
from flask.ext.mail import Mail, Message
from werkzeug.utils import secure_filename

from cryodex import Cryodex
import myapp
from persistence import Tourney, TourneyList, PersistenceManager,  Faction, Ship, ShipUpgrade, UpgradeType, Upgrade, \
    TourneyRound, RoundResult, TourneyPlayer, TourneyRanking
from rollup import Rollup
import xwingmetadata


app =  myapp.create_app()
UPLOAD_FOLDER = "static/tourneys"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set( ['png', 'jpg', 'jpeg', 'gif', 'html'])

is_maintenance_mode = False

here = os.path.dirname(__file__)
static_dir = os.path.join( here, app.config['UPLOAD_FOLDER'] )


MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['sozinsky@gmail.com']

session = myapp.db_connector.get_session()

mail = Mail(app)

@app.before_request
def check_for_maintenance():
    if is_maintenance_mode and request.path != url_for('down'):
        return redirect(url_for('down'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/test_mail")
def test_mail():
    msg = Message('test subject', sender=ADMINS[0], recipients=ADMINS)
    msg.body = 'text body'
    msg.html = '<b>HTML</b> body'
    with app.app_context():
        mail.send(msg)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/tourneys")
def tourneys():
    admin_on = request.args.get('admin')
    if admin_on is not None:
        admin_on = True
    else:
        admin_on = False
    summary = PersistenceManager(myapp.db_connector).get_tourney_summary()
    return render_template('tourneys.html', tourneys=summary, admin=admin_on )


@app.route("/new")
def new():
    return render_template('new.html')

def generate( rows ):
    for r in rows:
        yield ",".join(r) + "\n"

def get_tourney_lists_as_text(tourney, make_header=True ):

    rows   = []
    header =  xwingmetadata.header()

    if make_header:
        rows.append( header )

    tourney_date = "%d/%d/%d" % ( tourney.tourney_date.month, tourney.tourney_date.day, tourney.tourney_date.year )
    row_defaults = [ tourney.tourney_name, tourney.tourney_type, tourney_date ]

    for tourney_list in tourney.tourney_lists:
        if tourney_list.ships is None or len(tourney_list.ships) == 0:
            new_row = []
            new_row.extend ( row_defaults )
            for i in range (len(new_row), len(header)):
                new_row.append('')
            rows.append(new_row)
        else:
            for ship in tourney_list.ships:
                new_row = []
                new_row.extend( row_defaults )
                new_row.extend( [ tourney_list.player.player_name,
                                  tourney_list.faction.description,
                                  str(tourney_list.points),
                                  str(tourney_list.tourney_standing),
                                  str(tourney_list.tourney_elim_standing),
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
    return csv_response( rows, "all_lists_download.csv")


@app.route("/export_tourney_lists")
def export_tourney_lists():
    tourney_id = request.args.get('tourney_id')
    pm         = PersistenceManager(myapp.db_connector)
    tourney    = pm.get_tourney_by_id(tourney_id)

    ret = get_tourney_lists_as_text(tourney)
    return csv_response( ret, "tourney_list_download.csv")




@app.route("/delete_tourney")
def delete_tourney():
    tourney_name = request.args.get('tourney')
    pm = PersistenceManager(myapp.db_connector)
    pm.delete_tourney(tourney_name)
    return redirect(url_for('tourneys') )

def create_tourney(cryodex, tourney_name, tourney_date, tourney_type):

    pm = PersistenceManager(myapp.db_connector)
    t = Tourney(tourney_name=tourney_name, tourney_date=tourney_date, tourney_type=tourney_type)

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
                p1_tourney_list = lists[round_result.player1]
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
                                 list1_score=int(round_result.player1_score),
                                 list2_score=int(round_result.player2_score))
                pm.db_connector.get_session().add(rr)
    pm.db_connector.get_session().commit()

    #finally load the rankings
    for rank in cryodex.ranking.rankings:
        r = TourneyRanking( tourney   = t,
                            player    = players[rank.player_name],
                            rank      = rank.rank,
                            elim_rank = None,
                            mov       = rank.mov,
                            sos       = rank.sos,
                            score     = rank.score)
        pm.db_connector.get_session().add(r)
    pm.db_connector.get_session().commit()
    return t

@app.route("/add_tourney",methods=['POST'])
def add_tourney():

    #TODO: better edge testing against user input
    name   = request.form['name']
    type   = request.form['tourney_type']
    mmddyyyy = request.form['date'].split('/')
    date   = datetime.date( int(mmddyyyy[2]),int(mmddyyyy[0]), int(mmddyyyy[1]))

    tourney_report  = request.files['tourney_report']
    filename        = tourney_report.filename
    if tourney_report and allowed_file(filename):

        try:
            html = tourney_report.read()
            cryodex = Cryodex(html)
            t = create_tourney(cryodex, name, date, type )
            sfilename = secure_filename(filename)
            upload_folder = os.path.join( app.config['UPLOAD_FOLDER'], 'cryodex_uploads')
            tourney_report.save(os.path.join(upload_folder, sfilename + "." + str(t.id)) )
            return redirect(url_for('tourneys') )
        except Exception as err:
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

@app.route("/delete_list_and_retry")
def delete_list_and_retry():
    tourney_list_id = request.args.get('tourney_list_id')

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    pm.delete_tourney_list_details( tourney_list )
    return redirect( url_for('enter_list', tourney=tourney_list.tourney.id, tourney_list_id=tourney_list.id ) )


@app.route("/delete_list")
def delete_list():
    tourney_list_id = request.args.get('tourney_list_id')
    tourney_name    = request.args.get('tourney')
    admin           = request.args.get('admin')

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    pm.delete_tourney_list_details( tourney_list )
    return redirect( url_for('browse_list', tourney=tourney_name, admin=admin ) )



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
    return render_template('list_entry.html',
                           meta=m,
                           image_src=urllib.quote(tourney_list.image),
                           tourney_list=tourney_list,
                           tourney_list_id=tourney_list.id,
                           tourney_id=tourney.id )

@app.route("/add_squad",methods=['POST'])
def add_squad():
         data    = request.json['data']
         points  = request.json['points']
         faction = request.json['faction']

         tourney_id = request.args.get('tourney_id')
         tourney_list_id = request.args.get('tourney_list_id')

         pm = PersistenceManager(myapp.db_connector)
         tourney_list = pm.get_tourney_list(tourney_list_id)
         tourney_list.faction = Faction.from_string( faction )
         tourney_list.points  = points

         ships = []
         for squad_member in data:
             ship_pilot = pm.get_ship_pilot( squad_member['ship'], squad_member['pilot'] )
             ship       = Ship( ship_pilot_id=ship_pilot.id, tlist_id=tourney_list.id)
             tourney_list.ships.append( ship )
             for upgrade in squad_member['upgrades']:
                 ship_upgrade = ShipUpgrade( ship_id=ship.id,
                                             upgrade=Upgrade( upgrade_type= UpgradeType.from_string( upgrade['type'] ),
                                                                     name = upgrade['name'] ) )
                 ship.upgrades.append( ship_upgrade )
             ships.append( ship )

         pm.db_connector.get_session().add_all( ships )
         pm.db_connector.get_session().commit()

         return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list.id)

@app.route('/tourney_results')
def tourney_results():
    tourney_id = request.args.get('tourney_id')
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney_by_id(tourney_id)
    return render_template('tourney_results.html', tourney=tourney)

@app.route('/display_list')
def display_list():
    tourney_list_id = request.args.get('tourney_list_id')
    admin           = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    m = xwingmetadata.XWingMetaData()
    return render_template('list_display.html',
                           meta=m,
                           admin=admin,
                           image_src=urllib.quote(tourney_list.image),
                           tourney_list=tourney_list,
                           tourney_list_id=tourney_list.id,
                           tourney=tourney_list.tourney,
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
    rollup       = Rollup( PersistenceManager(myapp.db_connector), data['value'], data['eliminationOnly'] )
    chart_data   = rollup.rollup()
    return jsonify(data=chart_data,
                   title=data['value'] + rollup.title(),
                   firstCategory=rollup.first_category(),
                   secondCategory=rollup.second_category())


def to_float(dec):
    return float("{0:.2f}".format( float(dec) * float(100)))


@app.route("/charts")
def charts():
    return render_template('charts.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
