import sys
import collections
from decoder import decode
from persistence import League, Tier, Division, TierPlayer, LeagueMatch
from xws import XWSToJuggler, GeneralXWSFetcher

reload(sys)
sys.setdefaultencoding("utf-8")
import csv

CURRENT_VASSAL_LEAGUE_NAME = 'X-Wing Vassal League Season Six'

class CaseInsensitiveDict(collections.Mapping):
    def __init__(self, d):
        self._d = d
        self._s = dict((k.lower(), k) for k in d)
    def __contains__(self, k):
        return k.lower() in self._s
    def __len__(self):
        return len(self._s)
    def __iter__(self):
        return iter(self._s)
    def __getitem__(self, k):
        return self._d[self._s[k.lower()]]
    def actual_key_case(self, k):
        return self._s.get(k.lower())

class LeaguePlayersCSVImporter:


    def __init__(self,input):
        self.tsv_players = {}
        self.divisions = {}
        reader = csv.reader(input,delimiter='\t' )
        for row in reader:
            person_name = unicode(row[0].strip())
            player_name = unicode(row[1].strip())
            tier_name = row[2].strip()
            tier_number = row[3].strip()
            division_name = row[4].strip()
            division_letter = row[5].strip()
            self.tsv_players[player_name] = { 'person_name': person_name,
                                            'player_name' : player_name,
                                            'tier_name' : tier_name,
                                            'tier_number' : tier_number,
                                            'division_name' : division_name,
                                            'division_letter' : division_letter }
            if not self.divisions.has_key( division_name ):
                self.divisions[division_name] = { 'name': division_name, 'letter':division_letter, 'tier': tier_name}

        self.tsv_players = CaseInsensitiveDict(self.tsv_players)

class XWingVassalLeagueHelper:

    def __init__(self, name, number, players_data_file=None):
        self.name = name
        self.season_number = number
        if players_data_file:
            self.player_data = LeaguePlayersCSVImporter(players_data_file.stream)

    def create_league(self,pm,league):
        # create the leagues and then the tiers
        if league is None:
            league = League(name=self.name)
            pm.db_connector.get_session().add(league)

        if len(league.tiers) == 0:
            self.create_league_tiers(league, pm)

        self.create_divisions(pm, league)
        self.create_players(pm, league)
        #self.create_matchups(pm, league) do this after the league is "ready" to go


    def create_league_tiers(self,league, pm):
        tiers = {"Deep Core": "deepcore" + self.season_number,
                 "Core Worlds": "coreworlds" + self.season_number,
                 "Inner Rim": "innerrim" + self.season_number,
                 "Outer Rim": "outerrim" + self.season_number,
                 "Unknown Reaches": "unknownreaches" + self.season_number
                 }
        for tier_name in tiers.keys():
            tier_challonge_name = tiers[tier_name]
            lt = pm.get_tier(tier_challonge_name, league)
            if lt is None:
                lt = Tier(name=tier_name,
                          challonge_name=tier_challonge_name,
                          league=league)
                pm.db_connector.get_session().add(lt)
        pm.db_connector.get_session().commit()


    def create_divisions(self,pm, league):
        for name in self.player_data.divisions.keys():
            division = self.player_data.divisions[name]
            tier_name = division['tier'] + self.season_number
            tier = pm.get_tier(tier_name, league)
            if tier:
                d = Division()
                d.division_letter = division['letter']
                d.name = name
                d.tier = tier
                pm.db_connector.get_session().add(d)
        pm.db_connector.get_session().commit()


    def create_matchups(self, pm, league):
        for tier in league.tiers:
            for division in tier.divisions:
                players = division.players
                #simple round robin scheduling
                matchups = {}
                for player1 in players:
                    for player2 in players:
                        if player1.id == player2.id:
                            continue
                        k1 = str(player1.id) + "-vs-" + str(player2.id)
                        k2 = str(player2.id) + "-vs-" + str(player1.id)
                        if not matchups.has_key(k1) or \
                           not matchups.has_key(k2):
                            matchups[k1] = 1
                            matchups[k2] = 1
                            lm = LeagueMatch()
                            lm.player1_id = player1.id
                            lm.player2_id = player2.id
                            lm.tier_id = tier.id
                            lm.state = "open"
                            pm.db_connector.get_session().add(lm)
        pm.db_connector.get_session().commit()

    def create_players(self,pm, league):
        divisions_href = {}

        players = self.player_data.tsv_players.keys()
        for player_name in players:
            tsv_record = self.player_data.tsv_players[player_name]
            tier_player = TierPlayer()
            division_name = decode(tsv_record['division_name'])

            if not divisions_href.has_key(division_name):
                divisions_href[division_name] = pm.get_division(division_name, league)

            tier_player.division = divisions_href[division_name]
            tier_player.tier = tier_player.division.tier
            tier_player.name = player_name
            tier_player.person_name = decode(tsv_record['person_name'])
            pm.db_connector.get_session().add(tier_player)
        pm.db_connector.get_session().commit()


    def create_matchups_for_new_player(self, pm, new_player):
        division = new_player.division
        for opponent in division.players:
            if not opponent.id == new_player.id:
                #don't create it if it already exists
                self.create_league_match(division, new_player, opponent, pm)

    def create_league_match(self, division, player1, player2, pm, allow_duplicate=False ):
        match_exists = False
        if allow_duplicate == False:
            if len(player1.matches):
                for match in player1.matches:
                    if match.player1_id == player2.id or match.player2_id == player2.id:
                        return match
        lm = LeagueMatch()
        lm.player1 = player2
        lm.player2 = player1
        lm.state = 'open'
        lm.tier_id = division.tier.id
        pm.db_connector.get_session().add(lm)
        pm.db_connector.get_session().commit()
        return lm

    def add_player(self, pm, division_id, tier, email_address, player_name, person_name):
        tier_player = TierPlayer()
        tier_player.division = pm.get_division_by_id(division_id)
        tier_player.tier = tier
        tier_player.email_address = email_address
        tier_player.name = player_name
        tier_player.person_name = person_name

        pm.db_connector.get_session().add(tier_player)
        pm.db_connector.get_session().commit()

        # the player is added, now go set all the matches for this player in their division
        self.create_matchups_for_new_player(pm, tier_player)
        pm.db_connector.get_session().commit()
        return tier_player

    def merge_divisions(self, pm, from_division_id, to_division_id):

        from_division = pm.get_division_by_id(from_division_id)
        to_division   = pm.get_division_by_id(to_division_id)

        for player in from_division.players:
            to_division.players.append(player)

        pm.db_connector.get_session().commit()

        #do the matchups
        for player in from_division.players:
            self.create_matchups_for_new_player(pm, player)
        pm.db_connector.get_session().commit()

        #clear out the old division
        from_division.players = []
        pm.db_connector.get_session().commit()

        return to_division


    def update_escrowed_lists(self,pm, league, escrowed_lists):
        fetcher   = GeneralXWSFetcher()

        for el in escrowed_lists:
            player1_name = el['player1']
            player2_name = el['player2']
            list1        = el['list1']
            list2        = el['list2']

            player1      = pm.get_tier_player_by_name(player1_name, league.name)
            player2      = pm.get_tier_player_by_name(player2_name, league.name)
            if player1 and player2:
                match        = pm.get_match_by_players(league.id, player1.id, player2.id)

                if match:
                    dirty = False
                    if match.player1_list_url is None and list1 is not None:
                        match.player1_list_url = list1
                        try:
                            xws = fetcher.fetch(list1)
                            converter = XWSToJuggler(xws)
                            match.player1_list, _ = converter.convert(pm)
                            dirty = True
                        except Exception as err:
                            message = "unable to fetch list, reason: " + str(err)
                            print(message)

                    if match.player2_list_url is None and list2 is not None:
                        match.player2_list_url = list2
                        try:
                            xws = fetcher.fetch(list2)
                            converter = XWSToJuggler(xws)
                            match.player2_list, _ = converter.convert(pm)
                            dirty = True
                        except Exception as err:
                            message = "unable to fetch list, reason: " + str(err)
                            print(message)

                    if dirty:
                        pm.db_connector.get_session().add(match)

        pm.db_connector.get_session().commit()





