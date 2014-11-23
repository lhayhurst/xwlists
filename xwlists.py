from genericpath import isfile
import os
import urllib

from flask import render_template, request, url_for, redirect
import myapp
from persistence import Tourney, TourneyList, PersistenceManager

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

@app.route("/new")
def new():
    return render_template('new.html')

@app.route("/add_tourney",methods=['POST'])
def add_tourney():
    name   = request.form['name']
    folder = request.form['folder']
    #load all the files in the folder
    folder_path = os.path.join(static_dir, folder)
    tourney_files = {}
    for f in os.listdir(folder_path):
        if isfile(os.path.join(folder_path,f)):
            player_name = os.path.splitext(f)[0]
            tourney_files[player_name] = UPLOAD_FOLDER +  "/" + folder + "/" + f

    tourney = Tourney(tourney_name=name)
    myapp.db_connector.get_session().add(tourney)
    myapp.db_connector.get_session().commit()

    lists   = []
    for player_name in tourney_files.keys():
        f = tourney_files[player_name]
        tourney_list = TourneyList( tourney_id=tourney.id, image=f, player_name=player_name)
        lists.append( tourney_list )
    myapp.db_connector.get_session().add_all( lists )
    myapp.db_connector.get_session().commit()


    return render_template( 'tourney_load_results.html', name=name, lists=lists, num_lists=len(lists))

@app.route("/tourney_entry_status")
def tourney_entry_status():
    summary = PersistenceManager(myapp.db_connector).get_tourney_summary()
    return render_template('tourney_summary.html', tourneys=summary )

@app.route("/enter_list")
def enter_list():
    tourney_name = request.args.get('tourney')
    pm = PersistenceManager(myapp.db_connector)
    tourney = pm.get_tourney(tourney_name)
    tourney_list = pm.get_random_tourney_list(tourney)
    m = xwingmetadata.XWingMetaData()
    return render_template('worlds.html', meta=m, image_src=urllib.quote(tourney_list.image), tourney_list=tourney_list )

@app.route("/add_squad",methods=['POST'])
def add_squad():
    list = xwingmetadata.XWingList(request.form )
    print list.player
    print list.faction
    print list.points
    i = 1
    for ship in list.ships_submitted:
        for upgrade in ship.keys():
            print "Ship %d: %s : %s " % (i, upgrade, ship[upgrade ] )
    return redirect(url_for('new'))



#redirect '/' to new
@app.route('/')
def index():
    return redirect(url_for('new') )

if __name__ == '__main__':
    app.debug = True
    app.run()
