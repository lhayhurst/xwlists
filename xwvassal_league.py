

import os
import unittest
import sys
import collections
from decoder import decode
from persistence import League, Tier, Division, TierPlayer

reload(sys)
sys.setdefaultencoding("utf-8")
import csv

CURRENT_VASSAL_LEAGUE_NAME = 'X-Wing Vassal League Season Five'

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
            player_name = unicode(row[0].strip())
            person_name = unicode(row[1].strip())
            email_address = row[2].strip()
            time_zone = row[3].strip()
            tier_name = row[4].strip()
            tier_number = row[5].strip()
            division_name = row[6].strip()
            division_letter = row[7].strip()
            self.tsv_players[player_name] = { 'person_name': person_name,
                                            'email_address' : email_address,
                                            'player_name' : player_name,
                                            'time_zone' : time_zone,
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

        #self.create_divisions(pm, league)
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
            tier = pm.get_tier(division['tier'], league)
            if tier:
                d = Division()
                d.division_letter = division['letter']
                d.name = name
                d.tier = tier
                pm.db_connector.get_session().add(d)
        pm.db_connector.get_session().commit()


    def create_matchups(self, pm, league):
        #todo!
        pm.db_connector.get_session().commit()


    def create_players(self,pm, league):
        divisions_href = {}

        for tier in league.tiers:
            players = self.player_data.tsv_players.keys()
            for player_name in players:
                tsv_record = self.player_data.tsv_players[player_name]
                tier_player = TierPlayer()
                division_name = decode(tsv_record['division_name'])

                if not divisions_href.has_key(division_name):
                    divisions_href[division_name] = pm.get_division(division_name, league)

                tier_player.division = divisions_href[division_name]
                tier_player.tier = tier
                tier_player.name = player_name
                tier_player.email_address = decode(tsv_record['email_address'])
                tier_player.person_name = decode(tsv_record['person_name'])
                tier_player.timezone = decode(tsv_record['time_zone'])
                pm.db_connector.get_session().add(tier_player)
        pm.db_connector.get_session().commit()






