

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
