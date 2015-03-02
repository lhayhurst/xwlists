import json
from persistence import TourneyPlayer, TourneyRanking, TourneyList



def str2bool(v):
  return v.lower() in ("yes", "true", "True", "t", "1")

CREATE = "create"
EDIT   = "edit"
REMOVE = "remove"
DATA   = "data"

class RankingEditor:
    def __init__(self, pm, tourney):
        self.pm = pm
        self.tourney = tourney

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
            row['sos'] = ranking.sos
            row['list'] = ranking.pretty_print()
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
                                       "sos": ranking.sos, "dropped": ranking.dropped, "list":ranking.pretty_print()}} )
