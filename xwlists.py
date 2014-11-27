from genericpath import isfile
import os
import re
import urllib
import datetime

from flask import render_template, request, url_for, redirect, jsonify
import myapp
from persistence import Tourney, TourneyList, PersistenceManager, List, Faction, Ship, ShipUpgrade, UpgradeType

import xwingmetadata

app =  myapp.create_app()
UPLOAD_FOLDER = "static/tourneys"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set( ['png', 'jpg', 'jpeg', 'gif'])


here = os.path.dirname(__file__)
static_dir = os.path.join( here, app.config['UPLOAD_FOLDER'] )

ADMINS = ['sozinsky@gmail.com']

session = myapp.db_connector.get_session()

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

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

@app.route("/delete_tourney")
def delete_tourney():
    tourney_name = request.args.get('tourney')
    pm = PersistenceManager(myapp.db_connector)
    pm.delete_tourney(tourney_name)
    return redirect(url_for('tourneys') )

@app.route("/add_tourney",methods=['POST'])
def add_tourney():
    name   = request.form['name']
    folder = request.form['folder']
    type   = request.form['tourney_type']
    mmddyyyy = request.form['date'].split('/')
    date   = datetime.date( int(mmddyyyy[2]),int(mmddyyyy[1]), int(mmddyyyy[0]))

    #load all the files in the folder
    folder_path = os.path.join(static_dir, folder)
    tourney_files = {}
    for f in os.listdir(folder_path):
        if isfile(os.path.join(folder_path,f)):
            player_name = os.path.splitext(f)[0]
            tourney_files[player_name] = UPLOAD_FOLDER +  "/" + folder + "/" + f

    tourney = Tourney(tourney_name=name, tourney_date=date, tourney_type=type)
    myapp.db_connector.get_session().add(tourney)
    myapp.db_connector.get_session().commit()

    lists   = []
    for player_name in tourney_files.keys():
        f = tourney_files[player_name]

        try:

            match = re.match(r'^(.*?)\s+(\d+)',player_name)

            tourney_list = TourneyList( tourney_id=tourney.id,
                                        image=f,
                                        player_name=match.group(1),
                                        tourney_standing=match.group(2))
            lists.append( tourney_list )
        except:
            print ("unable to load file name %s" % ( player_name ))

    myapp.db_connector.get_session().add_all( lists )
    myapp.db_connector.get_session().commit()

    return redirect(url_for('tourneys') )

@app.route("/browse_list")
def browse_list():
    tourney_name = request.args.get('tourney')
    admin        = request.args.get('admin')
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney(tourney_name)
    tourney_lists = tourney.tourney_lists
    return render_template( 'tourney_lists.html', tourney=tourney, tourney_lists=tourney_lists, admin=admin)

@app.route("/delete_list")
def delete_list():
    tourney_list_id = request.args.get('tourney_list_id')
    tourney_name    = request.args.get('tourney')
    admin           = request.args.get('admin')

    pm = PersistenceManager(myapp.db_connector)
    tourney_list = pm.get_tourney_list(tourney_list_id)
    pm.delete_tourney_list( tourney_list )
    return redirect( url_for('browse_list', tourney=tourney_name, admin=admin ) )

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
         list = List(faction=Faction.from_string(faction), points=points)
         tourney_list.list = list
         pm.db_connector.get_session().add( list )
         pm.db_connector.get_session().commit()

         ships = []
         for squad_member in data:
             ship_pilot = pm.get_ship_pilot( squad_member['ship'], squad_member['pilot'] )
             ship       = Ship( ship_pilot_id=ship_pilot.id, list_id=list.id)
             list.ships.append( ship )
             for upgrade in squad_member['upgrades']:
                 ship_upgrade = ShipUpgrade( ship_id=ship.id,
                                             upgrade_type=UpgradeType.from_string( upgrade['type'] ),
                                             upgrade=upgrade['name'] )
                 ship.upgrades.append( ship_upgrade )
             ships.append( ship )

         pm.db_connector.get_session().add_all( ships )
         pm.db_connector.get_session().commit()

         return jsonify(tourney_id=tourney_id, tourney_list_id=tourney_list.id)

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
                           tourney=tourney_list.tourney )

@app.route('/')
def index():
    return redirect(url_for('tourneys') )

if __name__ == '__main__':
    app.debug = True
    app.run()
