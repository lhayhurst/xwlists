import re
from bs4 import BeautifulSoup
import collections
from persistence import RoundType

RANKINGS = 'Rankings'

H3    = 'h3'
DIV   = "div"
ELIM  = "Top"
ROUND = "Round"

class CryodexResult:
    def __init__(self, player1, player2, winner, player1_score, player2_score, bye, draw):
        self.player1       = player1
        self.player1_score = player1_score
        self.player2       = player2
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
        if self.type == ROUND:
            return RoundType.PRE_ELIMINATION
        elif self.type == ELIM:
            return RoundType.ELIMINATION
        else:
            return None

class CryodexRank:
    def __init__(self, rank, player_name, score, mov, sos):
        self.rank        = int(rank)
        self.elim_rank   = None
        self.player_name = player_name
        self.score       = int(score)
        self.mov         = int(mov)
        self.sos         = int(sos)
        self.dropped     = False


class CryodexRankings:
    def __init__(self, data):
        self.rankings = []
        firstRow = True
        for rec in data:
            if firstRow:
                firstRow = False
            else:
                rank  = rec[0]
                name  = rec[1]

                #some names look like this:
                #(D#3)Douglas Brito
                #so strip it off it is there

                score = rec[2]
                mov   = rec[3]
                sos   = rec[4]

                cr = CryodexRank( rank, name, score, mov, sos  )

                match = re.match( r'^\(D#\d\)', name)
                if match:
                    cr.player_name = re.sub(r'^\(D#\d\)', '', name)
                    cr.dropped = True

                self.rankings.append( cr )



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
        self.ranking = CryodexRankings( data )

    def __init__(self, html):
        self.players = {}
        self.html = html
        soup = BeautifulSoup( html )

        rounds = collections.OrderedDict()
        for section in soup.findAll(H3):
            if section.text == RANKINGS:
                self.parse_rankings(section.nextSibling)
                continue
            round_text = self.parse_round_text(section.text)
            if round_text:
                rounds[ section.text ] = []
            nextNode = section
            while True:
                nextNode = nextNode.nextSibling
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = ""
                if tag_name == DIV:
                    rounds[ section.text].append(nextNode.string)
                else:
                    round_text = self.parse_round_text(section.text)
                    break

        self.rounds = collections.OrderedDict()

        for round_name in rounds:
            round_results = rounds[round_name]
            round_info    = round_name.split()
            round_type    = round_info[0]
            round_number  = round_info[1]

            cr = CryodexRound( round_type, round_number )
            if not self.rounds.has_key( round_type ):
                self.rounds[round_type] = []
            self.rounds[round_type].append(cr)

            for result in round_results:
                match     = re.match(r'^(.*?)\s+VS\s+(.*?)\s+-\s+Match\s+Results:\s+(.*?)\s+is\s+the\s+winner', result)
                if match:
                    player1       = match.group(1)
                    player2       = match.group(2)
                    winner        = match.group(3)


                    player1_score = 0
                    player2_score = 0
                    match     = re.match(r'^.*?\s+VS\s+.*?\s+-\s+Match\s+Results:\s+.*?\s+is\s+the\s+winner\s+(\d+)\s+to\s+(\d+)', result)

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

                    cr.add_result( player1, player2, winner, int(player1_score), int(player2_score), bye=False, draw=False)
                else:
                    #player got a bye?
                    #Emmanuel Valadares has a BYE
                    match = re.match(r'^(.*?)\s+has\s+a\s+BYE', result )
                    if match:
                        player1  = match.group(1)
                        player2  = None
                        winner   = None
                        player1_score = None
                        player2_score = None

                        self.players[player1] = player1
                        cr.add_result( player1, player2, winner, player1_score, player2_score, bye=True, draw=False)
                    else:
                        #draw
                        #Kirlian Silvestre VS Joao Henrique - Match Results: Draw
                        match = re.match(r'^(.*?)\s+VS\s+(.*?)\s+-\s+Match\s+Results:\s+Draw', result)
                        if match:
                            player1 = match.group(1)
                            player2 = match.group(2)
                            winner  = None
                            player1_score = None
                            player2_score = None

                            self.players[player1] = player1
                            self.players[player2] = player2
                            cr.add_result( player1, player2, winner, player1_score, player2_score, bye=False, draw=True )

                        else:
                            #ok, give up
                            raise Exception("Cryodex parsing error, received a row that I don't know what to do with! Row is " + result )


        self.ranking.apply_elimination_results( self.rounds )