import decimal
import json
from persistence import TourneyPlayer, TourneyRanking, TourneyList



def str2bool(v):
  return v.lower() in ("yes", "true", "True", "t", "1")

CREATE = "create"
EDIT   = "edit"
REMOVE = "remove"
DATA   = "data"

class RoundResultsEditor:
    def __init__(self, pm, tourney, url_root, pre_elim=False):
        self.pm = pm
        self.tourney = tourney
        self.pre_elim=pre_elim
        self.url_root = url_root

    def create_result_record(self, result, round_num, row):
        row['result_id'] = result.id
        row['round'] = round_num
        row['player1_id'] = result.player1_name()
        row['result'] = result.get_result()
        row['player2_id'] = result.player2_name()
        row['player1_points_scored'] = result.get_list1_score()
        row['player2_points_scored'] = result.get_list2_score()
        row['player1_list'] = result.list1.pretty_print(self.url_root)
        row['player2_list'] = result.list2_pretty_print(self.url_root)

    def valid_score(self, score):
        return score >= 0 and score <= 100

    def get_and_set_json(self, request):
        #get the result
        result = self.pm.get_result_by_id( request.values['data[result_id]'])

        #and edit it
        round   = request.values['data[round]']
        result_val   = request.values['data[result]']
        p1_score     = request.values['data[player1_points_scored]']
        p2_score     = request.values['data[player2_points_scored]']

        result.edit( p1_score, p2_score, result_val)
        self.pm.db_connector.get_session().add(result)
        self.pm.db_connector.get_session().commit()

        row = {}
        self.create_result_record( result,round, row )
        return json.dumps(  { "row" : row  }  )





    def get_json(self):
        rounds = self.tourney.rounds
        filtered_rounds = []
        ret = {}
        rows = []
        ret[DATA] = rows

        for round in rounds:
            if self.pre_elim and round.is_pre_elim():
                filtered_rounds.append( round )
            elif not self.pre_elim and round.is_elim():
                filtered_rounds.append( round )

        for round in filtered_rounds:
            for result in round.results:
                row = {}
                self.create_result_record(result, round.round_num, row)
                rows.append( row )

        return json.dumps( ret  )




class RankingEditor:
    def __init__(self, pm, tourney, url_root):
        self.pm = pm
        self.tourney = tourney
        self.url_root = url_root

    def get_json(self):
        tourney_id = self.tourney.id
        players = self.tourney.tourney_players
        participant_count = self.tourney.participant_count
        rankings = self.tourney.rankings

        ret = {}
        data = []
        ret[DATA] = data

        if len(rankings) == 0:
            #tourney has not been initialized
            i = 1
            while i <= participant_count:
                player = TourneyPlayer( tourney_id=tourney_id, player_name="Player %d" % (i ) )
                self.pm.db_connector.get_session().add(player)


                ranking = TourneyRanking( tourney_id=tourney_id,  player=player,
                              score=0, mov=0, sos=0, rank=i, elim_rank=None, dropped=False )
                self.pm.db_connector.get_session().add(ranking)

                #create an empty tourney list for the player
                tourney_list = TourneyList( tourney_id=tourney_id, player=player )
                self.pm.db_connector.get_session().add(tourney_list)
                self.tourney.tourney_players.append(player)
                self.tourney.rankings.append(ranking)
                self.tourney.tourney_lists.append(tourney_list)
                i = i+1

            self.pm.db_connector.get_session().commit()

        for ranking in rankings:
            row = {}
            row['player_id'] = ranking.player_id
            row['player_name'] = ranking.player.get_player_name()
            row['score'] = ranking.score
            row['swiss_rank']  = ranking.rank
            row['dropped']     = ranking.dropped
            row['championship_rank'] = ranking.elim_rank
            row['mov'] = ranking.mov
            if ranking.sos is None:
                sos = None
            else:
                sos = "%.2f" % round(float(ranking.sos),2)
            row['sos'] = sos
            row['list'] = ranking.pretty_print(url_root=self.url_root)
            data.append(row)

        return json.dumps(ret)

    def set_and_get_json(self, request, player_name, event):
        #see https://editor.datatables.net/manual/server
        event_details = ""
        players           = self.tourney.tourney_players
        #get the client data
        action            = request.values['action']
        swiss_rank  = request.values['data[swiss_rank]']
        champ_rank  = request.values['data[championship_rank]']

        if len(champ_rank) == 0:
            champ_rank = None

        dropped     = str2bool(request.values['data[dropped]'])
        score       = request.values['data[score]']

        if len(score) == 0:
            score = None
        mov         = request.values['data[mov]']
        if len(mov) == 0:
            mov = None
        sos         = request.values['data[sos]']
        if len(sos) == 0:
            sos = None

        player_id = request.values['data[player_id]']
        if len(player_id) >0:
            player_id   = long(player_id)


        ranking     = None
        player = None

        for p in players:
            if p.id == player_id:
                player = p
                player.player_name = player_name
                break

        #figure out the actions
        if action == EDIT:
            #grab the rankings
            rankings = self.tourney.rankings
            #find it
            for r in rankings:
                if r.player_id == player_id:
                    #edit it
                    ranking = r
                    ranking.score = score
                    ranking.mov = mov
                    ranking.sos = sos
                    ranking.rank = swiss_rank
                    ranking.elim_rank = champ_rank
                    ranking.dropped = dropped
                    event.event_details = "edited player %s " % ( player.player_name )
                    break
        elif action == CREATE:
            player = TourneyPlayer( tourney_id=self.tourney.id, player_name=player_name)
            self.tourney.tourney_players.append(player)
            self.pm.db_connector.get_session().add(player)
            ranking = TourneyRanking( tourney_id=self.tourney.id,  player=player,
                          score=score, mov=mov, sos=sos, rank=swiss_rank, elim_rank=champ_rank, dropped=dropped )
            tourney_list = TourneyList( tourney_id=self.tourney.id, player=player )
            self.tourney.tourney_lists.append(tourney_list)
            self.pm.db_connector.get_session().add(tourney_list)
            self.tourney.rankings.append( ranking)
            self.pm.db_connector.get_session().add(ranking)
            event.event_details = "added player %s " % ( player.player_name )

        self.pm.db_connector.get_session().commit()

        return json.dumps( { "row" : { "player_id": player.id, "player_name": player.get_player_name(),
                                       "score": ranking.score, "swiss_rank" : ranking.rank,
                                       "championship_rank": ranking.elim_rank, "mov": ranking.mov,
                                       "sos": ranking.sos, "dropped": ranking.dropped, "list":ranking.pretty_print(self.url_root)}} )
