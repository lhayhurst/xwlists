import json
import os
import uuid
import MySQLdb

from flask import render_template, request, url_for, redirect, Response, make_response
from colorscale import colorscale
import myapp

from game_summary_stats import GameTape
from parser import LogFileParser
from persistence import Game, PersistenceManager, LuckResult, LuckMeasure
from plots.player_plots import LuckPlot, VersusPlot, AdvantagePlot, DamagePlot
from xwingmetadata import XWingMetaData
import xwingmetadata

app =  myapp.create_app()
UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set( ['png'])



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

@app.route("/worlds2014")
def worlds():
    m = XWingMetaData()
    return render_template('worlds.html', meta=m, image_src="static/worlds/Flight1/Aaron Bonar 5.jpeg" )

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


@app.route("/games" )
def games():
    try:
        games = PersistenceManager(myapp.db_connector).get_games(myapp.db_connector.get_session())
        return( render_template('games.html', num_games=len(games), games=games) )
    except MySQLdb.dbOperationalError:
        #give it another shot...
        games = PersistenceManager(myapp.db_connector).get_games(myapp.db_connector.get_session())
        return( render_template('games.html', num_games=len(games), games=games) )

@app.route("/editgames")
def editgames():
    try:
        games = PersistenceManager(myapp.db_connector).get_games(myapp.db_connector.get_session())
        return( render_template('games-edit.html', games=games) )
    except MySQLdb.dbOperationalError:
        #give it another shot...
        games = PersistenceManager(myapp.db_connector).get_games(myapp.db_connector.get_session())
        return( render_template('games-edit.html', games=games) )


@app.route('/new', methods=['GET'])
def new():
  return render_template('new.html')

#redirect '/' to new
@app.route('/')
def index():
    return redirect(url_for('new') )

def save_game_log( tape, is_good):
    dir = None
    if not is_good:
        dir = os.path.join( static_dir, "bad_chat_logs")
    else:
        dir = os.path.join( static_dir, "good_chat_logs")
    file = os.path.join( dir, str(uuid.uuid4() ) + ".txt" )
    fd = open( file, 'w' )
    fd.write( tape.encode('ascii', 'ignore') )
    fd.close()

@app.route('/add_game', methods=['POST'])
def add_game():
    tape  = request.form['chatlog']
    winner = request.form['winner']
    if len(tape) == 0:
        return redirect(url_for('new'))

    try:
        parser = LogFileParser(session)
        parser.read_input_from_string(tape)
        parser.run_finite_state_machine()

        if len(parser.get_players() ) is not 2:
            #this is not good, probably a result of a bad log file submission
            return render_template('new_after_error.html', players=", ".join(parser.get_players()), tape=tape, winner=winner)

        game = Game( session, parser.get_players())

        p1 = game.game_players[0]
        p2 = game.game_players[1]

        winning_player = None
        if winner is not None:
            if winner == p1.name:
                winning_player = p1
            elif winner == p2.name:
                winning_player = p2
        game.game_winner = winning_player

        for throw_result in parser.game_tape:
            game.game_throws.append(throw_result)


        session.add(game)
        session.commit()

        save_game_log( tape, is_good=True)
        return redirect( url_for('game', id=str(game.id) ) )

    except Exception as err:
        save_game_log( tape, is_good=False)
        return render_template( 'game_error.html', errortext=str(err) )

def get_game_tape_text(game, make_header=True):

    rows = []
    if make_header:
        rows.append( ['game_id', 'player_name', 'throw_id', 'attack_set_num', 'dice_num', 'roll_type', 'dice_color', 'dice_result'] )

    for throw in game.game_throws:
        for result in throw.results:
            row = [ str(game.id), throw.player.name, str(throw.id), str(throw.attack_set_num), str(result.dice_num), \
                    throw.throw_type.description, result.dice.dice_type.description, result.dice.dice_face.description]
            rows.append(row)
        for result in throw.results:
            for a in result.adjustments:
                arow = [ str(game.id), throw.player.name, str(throw.id), str(throw.attack_set_num), str(result.dice_num), \
                        a.adjustment_type.description, a.to_dice.dice_type.description, a.to_dice.dice_face.description]
                rows.append(arow)

    return rows

def generate( rows ):
    for r in rows:
        yield ",".join(r) + "\n"

@app.route('/download-dice')
def download_game():
    games = PersistenceManager(myapp.db_connector).get_games(myapp.db_connector.get_session())

    rows = []
    make_header = True
    for g in games:
        ret = get_game_tape_text(g, make_header)
        for r in ret:
            rows.append(r)
        if make_header is True:
            make_header = False

    disposition = "attachment; filename=all_dice.csv"
    return Response(generate(rows), mimetype='text/csv', headers={'Content-Disposition': disposition} )

@app.route('/delete_game')
def delete_game():
    id = str(request.args.get('id'))
    game = PersistenceManager(myapp.db_connector).get_game(session,id)
    if game == None:
        return redirect(url_for('new'))
    #doing this manually as I banged my head against the wall trying to get it to work using the sql alchemy cascade logic...
    luck_results = PersistenceManager(myapp.db_connector).get_luck_score(session, game.id)
    if luck_results is not None:
        for lr in luck_results:
            myapp.db_connector.get_session().delete(lr)

    for throw in game.game_throws:
        for result in throw.results:
            for adjustment in result.adjustments:
                myapp.db_connector.get_session().delete(adjustment)
            myapp.db_connector.get_session().delete(result)
        myapp.db_connector.get_session().delete(throw)

    myapp.db_connector.get_session().delete(game)
    myapp.db_connector.get_session().commit()




    return redirect(url_for('editgames'))

@app.route('/leaderboard')
def leaderboard():
    bottom_ten_greens = PersistenceManager(myapp.db_connector).get_worst_green_luck_scores(myapp.db_connector.get_session()).all()[0:10]
    bottom_ten_reds   = PersistenceManager(myapp.db_connector).get_worst_red_luck_scores(myapp.db_connector.get_session()).all()[0:10]
    top_ten_greens    = PersistenceManager(myapp.db_connector).get_best_green_luck_scores(myapp.db_connector.get_session()).all()[0:10]
    top_ten_reds      = PersistenceManager(myapp.db_connector).get_best_red_luck_scores(myapp.db_connector.get_session()).all()[0:10]


    return render_template( 'leaderboard.html',
                            bottom_ten_greens=bottom_ten_greens,
                            bottom_ten_reds=bottom_ten_reds,
                            top_ten_greens=top_ten_greens,
                            top_ten_reds=top_ten_reds)

def calculate_luck_result(game, game_tape):
    if game_tape is None:
        try:
            game_tape = GameTape(game)
            game_tape.score()
        except:
            print "couldn't score game id {0}.".format(game.id)
            return None
    for player in game.game_players:
        luck_result = LuckResult()
        luck_result.measure = LuckMeasure.DOZIN
        luck_result.player = player
        luck_result.game = game

        initial_red_scores = game_tape.initial_red_scores(player)
        luck_result.initial_attack_luck = initial_red_scores[-1]

        final_red_scores = game_tape.final_red_scores(player)
        luck_result.final_attack_luck = final_red_scores[-1]

        initial_green_scores = game_tape.initial_green_scores(player)
        luck_result.initial_defense_luck = initial_green_scores[-1]

        final_green_scores = game_tape.final_green_scores(player)
        luck_result.final_defense_luck = final_green_scores[-1]

        return luck_result

@app.route('/populate_luck_scores')
def populate_luck_scores():
    games = PersistenceManager(myapp.db_connector).get_games(myapp.db_connector.get_session())
    for game in games:
        luck_result = calculate_luck_result(game, score_tape=True)
        if luck_result is not None:
            myapp.db_connector.get_session().add( luck_result )
    myapp.db_connector.get_session().commit()
    return redirect(url_for('editgames'))



@app.route('/game')
def game():
    id = str(request.args.get('id'))
    pm = PersistenceManager(myapp.db_connector)
    game = pm.get_game(session,id)
    if game == None:
        return redirect(url_for('new'))

    player1 = game.game_players[0]
    player2 = game.game_players[1]

    winning_player = "Unknown"
    if game.game_winner is not None:
        winning_player = game.game_winner.name

    #summary_stats = GameSummaryStats(game)
    game_tape = GameTape(game)
    game_tape.score()

    luck_result = pm.get_luck_score(session, game.id)

    if luck_result is None:

        luck_result = calculate_luck_result(game, game_tape)
        if luck_result is not None:
            myapp.db_connector.get_session().add(luck_result)
            myapp.db_connector.get_session().commit()

    return render_template( 'game_summary.html',
                            game=game,
                            player1=player1,
                            player2=player2,
                            winner=winning_player,
                            game_tape=game_tape,
                            colorscale=colorscale() )

@app.route('/damage')
def damage():
    id = str(request.args.get('game_id'))
    game = PersistenceManager().get_game(session, id)

    if game.game_tape is None:
        game_tape = GameTape(game)
        game_tape.score()

    dp = DamagePlot( game )
    output = dp.plot()
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/advantage')
def advantage():
    id = str(request.args.get('game_id'))
    use_initial = int(request.args.get('initial'))
    game = PersistenceManager().get_game(session,id)

    ap = AdvantagePlot( game, use_initial )
    output = ap.plot()
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/versus')
def versus():
    id = str(request.args.get('game_id'))
    game = PersistenceManager().get_game(session,id)

    attacker_id = long(request.args.get('attacker'))
    defender_id = long(request.args.get('defender'))

    vp = VersusPlot( game, attacker_id, defender_id)
    output = vp.plot()
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/luck_graph')
def luck_graph():
    id = str(request.args.get('game_id'))
    game = PersistenceManager().get_game(session,id)

    player_id = long(request.args.get('player'))
    dice_type = request.args.get('dice_type')

    lp = LuckPlot( game, player_id, dice_type)
    return lp.plot()



if __name__ == '__main__':
    app.debug = True
    app.run()
