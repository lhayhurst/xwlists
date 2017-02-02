

import os
import unittest
import sys
import collections
from decoder import decode

reload(sys)
sys.setdefaultencoding("utf-8")
from challonge_helper import ChallongeHelper
import myapp
from persistence import PersistenceManager, TierPlayer, Division, LeagueMatch
import csv

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

class ChallongeMatchCSVImporter:


    def __init__(self,input):
        self.tsv_players = {}
        self.divisions = {}
        reader = csv.reader(input,delimiter='\t' )
        for row in reader:
            challonge_name = unicode(row[0].strip())
            person_name = unicode(row[1].strip())
            email_address = row[2].strip()
            time_zone = row[3].strip()
            tier_name = row[4].strip()
            tier_number = row[5].strip()
            division_name = row[6].strip()
            division_letter = row[7].strip()
            self.tsv_players[challonge_name] = { 'person_name': person_name,
                                            'email_address' : email_address,
                                            'challonge_name' : challonge_name,
                                            'time_zone' : time_zone,
                                            'tier_name' : tier_name,
                                            'tier_number' : tier_number,
                                            'division_name' : division_name,
                                            'division_letter' : division_letter }
            if not self.divisions.has_key( division_name ):
                self.divisions[division_name] = { 'name': division_name, 'letter':division_letter, 'tier': tier_name}

        self.tsv_players = CaseInsensitiveDict(self.tsv_players)

def create_divisions(c, pm, league):
    for name in c.divisions.keys():
        division = c.divisions[name]
        tier = pm.get_tier(division['tier'],league)
        d = Division()
        d.challonge_name = division['letter']
        d.name = name
        d.tier = tier
        pm.db_connector.get_session().add(d)
    pm.db_connector.get_session().commit()

def create_default_match_result(match_result, tier, pm):
    p1id = match_result['player1_id']
    p2id = match_result['player2_id']
    player1 = pm.get_tier_player_by_group_id(p1id)
    player2 = pm.get_tier_player_by_group_id(p2id)
    if player1 is None or player2 is None:
        #one of the byes, ignore it
        return None
    #TODO: freak out if not found
    lm = LeagueMatch()
    lm.tier_id = tier.id
    lm.player1 = player1
    lm.player2 = player2
    lm.challonge_match_id = match_result['id']
    lm.state = match_result['state']

    scores_csv = match_result['scores_csv']
    p1_score = None
    p2_score = None
    if scores_csv is not None and len(scores_csv) > 0:
        scores_csv = str(scores_csv)
        scores = str.split(scores_csv, '-')
        lm.player1_score = scores[0]
        lm.player2_score = scores[1]

    return lm

def create_matchups(c, pm, ch, league):
    for tier in league.tiers:
        matchups = ch.match_index(tier.get_challonge_name())
        for matchup in matchups:
            matchup = matchup['match']
            dbmr = create_default_match_result(matchup, tier, pm)
            if dbmr is not None:
                pm.db_connector.get_session().add(dbmr)
    pm.db_connector.get_session().commit()

def create_players(c, pm, ch, league):
    divisions_href = {}
    cin = ""

    for tier in league.tiers:
        players = ch.participant_index(tier.get_challonge_name())
        for player in players:
            lookup_name = None
            player = player['participant']
            challonge_username_ = player['challonge_username']
            checked_in = player['checked_in']
            if challonge_username_ is None or checked_in is False:
                lookup_name = player['display_name']
#                print "player %s has not checked in " % ( lookup_name)
            else:
                lookup_name = challonge_username_
            if not c.tsv_players.__contains__(lookup_name):
                print "just couldn't find player %s" % ( lookup_name)
            else:
                # we're good to go
                tsv_record = c.tsv_players[lookup_name]
                if checked_in is False:
                    cin = cin + decode(tsv_record['email_address']) + ","

                # create the player record
                tier_player = TierPlayer()
                division_name = decode(tsv_record['division_name'])
                print "looking up division %s for player %s" % (division_name, lookup_name)

                if not divisions_href.has_key(division_name):
                    divisions_href[division_name] = pm.get_division(division_name, league)
                tier_player.division = divisions_href[division_name]
                tier_player.tier = tier_player.division.tier
                tier_player.challengeboards_handle = decode(tsv_record['challengeboards_name'])
                tier_player.challonge_id = player['id']
                print player['group_player_ids'][0]
                tier_player.group_id = player['group_player_ids'][0]
                tier_player.name = lookup_name
                tier_player.email_address = decode(tsv_record['email_address'])
                tier_player.person_name = decode(tsv_record['person_name'])
                tier_player.reddit_handle = decode(tsv_record['reddit_handle'])
                tier_player.timezone = decode(tsv_record['time_zone'])
                pm.db_connector.get_session().add(tier_player)
    pm.db_connector.get_session().commit()

if __name__ == "__main__":
    c = ChallongeMatchCSVImporter(sys.argv[1])
    pm  = PersistenceManager( myapp.db_connector )
    challonge_user = os.getenv('CHALLONGE_USER')
    challonge_key  = os.getenv('CHALLONGE_API_KEY')
    ch = ChallongeHelper(challonge_user, challonge_key)
    league = pm.get_league( "X-Wing Vassal League Season Four")

    #create all the divisions for each tier
    create_divisions(c,pm,league)
    create_players(c, pm, ch, league)
    create_matchups(c, pm, ch, league)
