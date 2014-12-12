import re
from bs4 import BeautifulSoup
import collections
from persistence import RoundType

RANKINGS = 'Rankings'

H3 = 'h3'
DIV = "div"

class CryodexResult:
    def __init__(self, player1, player2, winner, player1_score, player2_score):
        self.player1       = player1
        self.player1_score = player1_score
        self.player2       = player2
        self.player2_score = player2_score
        self.winner        = winner

class CryodexRound:
    def __init__(self, type, number):
        self.type   = type
        self.number = number
        self.results = []

    def add_result( self, player1, player2, winner, player1_score, player2_score):
        result = CryodexResult( player1, player2, winner, player1_score, player2_score)
        self.results.append( result )

    def get_round_type(self):
        if self.type == 'Round':
            return RoundType.PRE_ELIMINATION
        elif self.type == 'Top':
            return RoundType.ELIMINATION
        else:
            return None

class CryodexRank:
    def __init__(self, rank, player_name, score, mov, sos):
        self.rank        = rank
        self.player_name = player_name
        self.score       = score
        self.mov         = mov
        self.sos         = sos


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
                score = rec[2]
                mov   = rec[3]
                sos   = rec[4]
                self.rankings.append( CryodexRank( rank, name, score, mov, sos  ))


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
                match     = re.match(r'^(\w+)\s+VS\s+(\w+)\s+-\s+Match\s+Results:\s+(\w+)\s+is\s+the\s+winner\s+(\d+)\s+to\s+(\d+)', result)
                if match:
                    player1       = match.group(1)
                    player2       = match.group(2)
                    winner        = match.group(3)
                    player1_score = match.group(4)
                    player2_score = match.group(5)

                    self.players[player1] = player1
                    self.players[player2] = player2

                    cr.add_result( player1, player2, winner, player1_score, player2_score)