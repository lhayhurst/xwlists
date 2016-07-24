import json
import re
import unittest
import collections
from BeautifulSoup import BeautifulSoup
from persistence import RoundType

RANKINGS = 'Rankings'

H3    = 'h3'
DIV   = "div"
ELIM  = "Top"
ROUND = "Round"
SWISS = 'swiss'
ELIMINATION = 'elimination'

class CryodexResult:
    def __init__(self, player1, player2, winner, player1_score, player2_score, bye, draw):
        self.player1       = player1.strip()
        self.player1_score = player1_score
        if player2 is not None:
            self.player2       = player2.strip()
        self.player2_score = player2_score
        self.winner        = winner
        self.bye           = bye
        self.draw          = draw

class CryodexRound:
    def __init__(self, type, number):
        self.type   = type
        self.number = number
        self.results = []

    def add_result( self, player1, player2, winner, player1_score, player2_score, bye=False, draw=False):
        result = CryodexResult( player1, player2, winner, player1_score, player2_score, bye, draw)
        self.results.append( result )

    def get_round_type(self):
        if self.type == ROUND or self.type == SWISS:
            return RoundType.PRE_ELIMINATION
        elif self.type == ELIM or self.type == ELIMINATION:
            return RoundType.ELIMINATION
        else:
            return None

class CryodexRank:
    def __init__(self, player_name, rank=None, elim_rank=None, score=None, mov=None, sos=None, dropped=False, list_id=None ):
        self.rank        = int(rank)
        self.elim_rank   = elim_rank
        self.player_name = player_name
        self.score       = int(score)
        self.mov         = int(mov)
        self.sos         = sos
        self.dropped     = dropped
        self.list_id     = list_id


class CryodexRankings:

    def fromJson(self, data):
        self.rankings = []
        for rank in data:
            name  = rank['name']
            name = name.strip()
            score = rank['score']
            mov   = rank['mov']
            sos   = rank['sos']
            swiss = None
            elim  = None
            dropped = False
            ranks = rank['rank']
            list_id = None
            if ranks.has_key( 'swiss'):
                swiss = ranks['swiss']
            if ranks.has_key('elimination'):
                elim  = ranks['elimination']
            if rank.has_key('dropped'):
                dropped = True
            if rank.has_key( "list-id" ):
                list_id = rank['list-id']
            cr = CryodexRank( name, swiss, elim, score, mov, sos, dropped, list_id )
            self.rankings.append(cr)

    def __init__(self, data):
        self.fromJson(data)

    def apply_elimination_results(self, rounds):
        if not rounds.has_key( RoundType.ELIMINATION ):
            return
        elim_rounds = rounds[RoundType.ELIMINATION]
        i = 0
        for round in elim_rounds:
            i = i + 1
            elim_rank = round.number
            for result in round.results:
                winner    = result.winner
                loser     = None
                if winner == result.player1:
                    loser = result.player2
                else:
                    loser = result.player1
                #set the ranking of the player
                for rank in self.rankings:
                    if rank.player_name == loser:
                        rank.elim_rank = int(elim_rank)
                        break

                #set the winner if its the last one
                if i == len(elim_rounds):
                    for rank in self.rankings:
                        if rank.player_name == winner:
                            rank.elim_rank = 1
                            break



class Cryodex:

    def parse_round_text(self, text):
        match = re.match(r'^(\w+)\s+(\d+)', str(text))
        if match:
            round_type = match.group(1)
            round_num  = match.group(2)
            return { 'type': round_type, 'num': round_num }
        return None

    def processJson(self, data):
        json_data = json.loads(data)
        if json_data is None:
            raise Exception("Unable to parse json data: " + data )

        if json_data.has_key('tournament'): #for the new tournament api
            json_data = json_data['tournament']
        players = json_data['players']

        #init the player member
        for player in players:
            self.players[player['name'].strip()] = player['name'].strip()

        #and the ranking member
        self.ranking = CryodexRankings( players )

        #and finally the rounds member
        rounds = json_data['rounds']
        for round in rounds:
            round_type   = round['round-type']
            round_number = round['round-number']

            cr = CryodexRound(round_type, round_number)
            if not self.rounds.has_key(cr.get_round_type()):
                self.rounds[cr.get_round_type()] = []
            self.rounds[cr.get_round_type()].append(cr)


            for match in round['matches']:
                match_result = match['result']
                player1      = match['player1']
                p1points     = match['player1points']

                if match_result == 'bye':
                    cr.add_result( player1, None, None, p1points, None, bye=True, draw=False)
                elif match_result == 'draw':
                    player2      = match['player2']
                    p2points     = match['player2points']
                    cr.add_result( player1, player2, None, p1points, p2points, bye=False, draw=True)
                elif match_result == 'win':
                    winner = None
                    player2      = match['player2']
                    p2points     = match['player2points']
                    if p1points > p2points:
                        winner = player1
                    else:
                        winner = player2

                    cr.add_result( player1, player2, winner, p1points, p2points, bye=False, draw=False)

    def __init__(self, data, filename):
        self.players = {}
        self.rounds = collections.OrderedDict()
        self.ranking = None
        self.data = data

        if filename.endswith("json"):
            self.processJson(data)
        else:
            raise Exception("Unable to parse cryodex filename " + filename + ", reason: unknown file type (expecting .html or .json)" )




class CryodexTests(unittest.TestCase):

    #@unittest.skip("because")
    def testJsonImport(self):
        fname = "static/tourneys/XWingTournament.json"
        f = open(fname)
        json = f.read()
        c = Cryodex(json, fname)

        #check everyone's rankings
        rankings = c.ranking.rankings
        self.assertEqual(19, len(rankings))

        first = rankings[0]
        self.assertEqual( 1, first.rank)
        self.assertEqual( 2, first.elim_rank)
        self.assertEqual( "Lyle Hayhurst", first.player_name)
        self.assertEqual( 20, first.score)
        self.assertEqual( 622, first.mov)
        self.assertEqual( 50, first.sos)
        self.assertEqual( False, first.dropped )

        second = rankings[1]
        self.assertEqual( 2, second.rank)
        self.assertEqual( 4, second.elim_rank)
        self.assertEqual( "Brandon Prokos", second.player_name)
        self.assertEqual( 15, second.score)
        self.assertEqual( 647, second.mov)
        self.assertEqual( 45, second.sos)
        self.assertEqual( False, second.dropped )

        last = rankings[18]
        self.assertEqual( 0, last.rank)
        self.assertEqual( None, last.elim_rank)
        self.assertEqual( "Steven Smith", last.player_name)
        self.assertEqual( 0, last.score)
        self.assertEqual( 0, last.mov)
        self.assertEqual( 5, last.sos)
        self.assertEqual( True, last.dropped )



        self.assertEqual( 19, len(c.players.keys()))
        self.assertTrue( c.rounds.has_key(RoundType.PRE_ELIMINATION))
        self.assertTrue( c.rounds.has_key(RoundType.ELIMINATION))

        rounds = c.rounds[RoundType.PRE_ELIMINATION]
        self.assertEqual( 4,len(rounds) )

        r1 = rounds[0]
        self.assertEqual( 1, int(r1.number))
        r1_results = r1.results
        self.assertEqual( 10, len(r1_results) )

        m1 = r1_results[0]
        self.assertEqual( 'Lyle Hayhurst', m1.winner )
        self.assertEqual( 'Brandon Prokos', m1.player2)
        self.assertEqual( 100, m1.player1_score)
        self.assertEqual( 48, m1.player2_score)

        m2 = r1_results[1]
        self.assertEqual( 'Zach Carriger', m2.winner )
        self.assertEqual( 'Phil Kalata', m2.player2)
        self.assertEqual( 32, m2.player1_score)
        self.assertEqual( 0, m2.player2_score)

        m7 = r1_results[8]
        self.assertEqual( True, m7.bye )
        self.assertEqual( 'Louie Fabicon', m7.player1)


        #check the elimination round
        rounds = c.rounds[RoundType.ELIMINATION]
        self.assertEqual( 3, len(rounds))
        r1 = rounds[0]
        self.assertEqual( 8, int(r1.number))
        r1_results = r1.results
        self.assertEqual( 4, len(r1_results) )

        m1 = r1_results[0]
        self.assertEqual( 'Lyle Hayhurst', m1.winner )
        self.assertEqual( 'Matt Babiash', m1.player2)
        self.assertEqual( 100, m1.player1_score)
        self.assertEqual( 80, m1.player2_score)

        m2 = r1_results[1]
        self.assertEqual( 'Phil Kalata', m2.player1 )
        self.assertEqual( 'David Pontier', m2.player2)
        self.assertEqual( 'David Pontier', m2.winner)

        self.assertEqual( 0, m2.player1_score)
        self.assertEqual( 100, m2.player2_score)

        m3 = r1_results[2]
        self.assertEqual( 'Dom Cairo', m3.player1 )
        self.assertEqual( 'Russell Roberts', m3.player2)
        self.assertEqual( 'Dom Cairo', m3.winner)

        self.assertEqual( 100, m3.player1_score)
        self.assertEqual( 0, m3.player2_score)



    #@unittest.skip("because")
    def testHtmlImport(self):

        fname = "static/tourneys/mapril.html"
        f = open(fname)
        html = f.read()

        c = Cryodex(html, fname)

        self.assertEqual( 5, len( c.players.keys() ))

        self.assertTrue( c.rounds.has_key(RoundType.PRE_ELIMINATION))
        rounds = c.rounds[RoundType.PRE_ELIMINATION]
        self.assertEqual( 5,len(rounds) )
        r1 = rounds[0]
        self.assertEqual( 1, int(r1.number))
        r1_results = r1.results
        self.assertEqual( 3, len(r1_results) )

        m1 = r1_results[0]
        self.assertEqual( 'Mapril', m1.winner )
        self.assertEqual( 'Fernando', m1.player2)
        self.assertEqual( 99, m1.player1_score)
        self.assertEqual( 33, m1.player2_score)

        m2 = r1_results[1]
        self.assertEqual( 'Alex', m2.winner )
        self.assertEqual( 'Antonio', m2.player2)
        self.assertEqual( 100, m2.player1_score)
        self.assertEqual( 52, m2.player2_score)

        m3 = r1_results[2]
        self.assertEqual( True, m3.bye )
        self.assertEqual( '48K', m3.player1)

#        rounds = c.rounds[RoundType.ELIMINATION]
#        self.assertEqual( 2, len(rounds))




    def testByeCase(self):
        # 1: 48K has a BYE
        # 48K has a bye
        input = "48K has a bye"
        bye_expr = re.compile( r'^(?:\d+:)?\s*(.*?)\s+has\s+a\s+bye\s*$', re.IGNORECASE )
        match = bye_expr.match(input)
        self.assertTrue(match)
        self.assertTrue(match.group(1))
        self.assertEqual( "48K", match.group(1))
        input = "1: 48K has a BYE"
        match = bye_expr.match(input)
        self.assertTrue(match)
        self.assertTrue(match.group(1))
        self.assertEqual( "48K", match.group(1))



if __name__ == "__main__":
    unittest.main()
