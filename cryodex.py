import json
import re
import unittest
from bs4 import BeautifulSoup
import collections
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
    def __init__(self, player_name, rank=None, elim_rank=None, score=None, mov=None, sos=None, dropped=False ):
        self.rank        = int(rank)
        self.elim_rank   = elim_rank
        self.player_name = player_name
        self.score       = int(score)
        self.mov         = int(mov)
        self.sos         = int(sos)
        self.dropped     = dropped


class CryodexRankings:
    def parseHtml(self, data):
        firstRow = True
        for rec in data:
            if firstRow:
                firstRow = False
            else:
                rank = rec[0]
                name = rec[1]

                #some names look like this:
                #(D#3)Douglas Brito
                #so strip it off it is there

                score = rec[2]
                mov = rec[3]
                sos = rec[4]

                cr = CryodexRank( name, rank, None , score, mov, sos)

                match = re.match(r'^\(D#\d\)', name)
                if match:
                    print "player with a bye:" + name
                    cr.player_name = re.sub(r'^\(D#\d\)', '', name)
                    print "stripped to:" + cr.player_name

                    cr.dropped = True

                self.rankings.append(cr)

    def fromJson(self, data):
        for rank in data:
            name  = rank['name']
            score = rank['score']
            mov   = rank['mov']
            sos   = rank['sos']
            swiss = None
            elim  = None
            dropped = False
            ranks = rank['rank']
            if ranks.has_key( 'swiss'):
                swiss = ranks['swiss']
            if ranks.has_key('elimination'):
                elim  = ranks['elimination']
            if rank.has_key('dropped'):
                dropped = True
            cr = CryodexRank( name, swiss, elim, score, mov, sos, dropped )
            self.rankings.append(cr)

    def __init__(self, data, ishtml):
        self.rankings = []
        if ishtml:
            self.parseHtml(data)
        else:
            self.fromJson(data)

    def apply_elimination_results(self, rounds):
        if not rounds.has_key( ELIM ):
            return
        elim_rounds = rounds[ELIM]
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

    def parse_rankings(self, table):
        data = []
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
        self.ranking = CryodexRankings( data, ishtml=True )

    def parseHtml(self, data):
        soup = BeautifulSoup(data)
        rounds = collections.OrderedDict()
        for section in soup.findAll(H3):
            if section.text == RANKINGS:
                self.parse_rankings(section.nextSibling)
                continue
            round_text = self.parse_round_text(section.text)
            if round_text:
                rounds[section.text] = []
            nextNode = section
            while True:
                nextNode = nextNode.nextSibling
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = ""
                if tag_name == DIV:
                    rounds[section.text].append(nextNode.string)
                else:
                    round_text = self.parse_round_text(section.text)
                    break
        for round_name in rounds:
            round_results = rounds[round_name]
            round_info = round_name.split()
            round_type = round_info[0]
            round_number = round_info[1]

            cr = CryodexRound(round_type, round_number)
            if not self.rounds.has_key(cr.get_round_type()):
                self.rounds[cr.get_round_type()] = []
            self.rounds[cr.get_round_type()].append(cr)

            for result in round_results:
                match = re.match(r'^(?:\d+:)?\s*(.*?)\s+VS\s+(.*?)\s+-\s+Match\s+Results:\s+(.*?)\s+is\s+the\s+winner',
                                 result)
                if match:
                    player1 = match.group(1)
                    player2 = match.group(2)
                    winner = match.group(3)

                    player1_score = 0
                    player2_score = 0
                    match = re.match(
                        r'^(?:\d+:)?.*?\s+VS\s+.*?\s+-\s+Match\s+Results:\s+.*?\s+is\s+the\s+winner\s+(\d+)\s+to\s+(\d+)',
                        result)

                    if match:
                        player1_score = match.group(1)
                        player2_score = match.group(2)
                    else:
                        if winner == player1:
                            player1_score = 100
                            player2_score = 0
                        else:
                            player1_score = 0
                            player2_score = 100

                    self.players[player1] = player1
                    self.players[player2] = player2

                    cr.add_result(player1, player2, winner, int(player1_score), int(player2_score), bye=False,
                                  draw=False)
                else:
                    #player got a bye?
                    #Emmanuel Valadares has a BYE
                    #or, the most awful case:
                    #1: 48K has a BYE
                    match = re.match(r'^(?:\d+:)?\s*(.*?)\s+has\s+a\s+BYE\s*$', result)
                    if match:
                        player1 = match.group(1)
                        player2 = None
                        winner = None
                        player1_score = None
                        player2_score = None

                        self.players[player1] = player1
                        cr.add_result(player1, player2, winner, player1_score, player2_score, bye=True, draw=False)
                    else:
                        #draw
                        #Kirlian Silvestre VS Joao Henrique - Match Results: Draw
                        match = re.match(r'^(?:\d+:)?\s*(.*?)\s+VS\s+(.*?)\s+-\s+Match\s+Results:\s+Draw', result)
                        if match:
                            player1 = match.group(1)
                            player2 = match.group(2)
                            winner = None
                            player1_score = None
                            player2_score = None

                            self.players[player1] = player1
                            self.players[player2] = player2
                            cr.add_result(player1, player2, winner, player1_score, player2_score, bye=False, draw=True)

                        else:
                            #ok, give up
                            raise Exception(
                                "Cryodex parsing error, received a row that I don't know what to do with! Row is " + result)

    def processJson(self, data):
        json_data = json.loads(data)
        if json_data is None:
            raise Exception("Unable to parse json data: " + data )
        players = json_data['players']

        #init the player member
        for player in players:
            self.players[player['name']] = player['name']

        #and the ranking member
        self.ranking = CryodexRankings( players, ishtml=False)

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
        elif filename.endswith("html"):
            self.parseHtml(data)
        else:
            raise Exception("Unable to parse cryodex filename " + filename + ", reason: unknown file type (expecting .html or .json)" )
        self.ranking.apply_elimination_results(self.rounds)



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
        self.assertEqual( 2, last.dropped )



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
