import os
from sqlalchemy import func
from cryodex import Cryodex
from myapp import db_connector
from persistence import PersistenceManager, Ship, Tourney, TourneyList, TourneyRound, RoundResult, TourneyRanking, \
    TourneyPlayer
from rollup import Rollup

__author__ = 'lhayhurst'
import sys
import unittest


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):

        self.pm = PersistenceManager(db_connector)
        self.session = db_connector.get_session()

    def tearDown(self):

        self.session.close_all()


class DbPort(DatabaseTestCase):

    @unittest.skip("because")
    def testPortPlayerTable(self):
        tourneys = self.pm.get_tourneys()
        for tourney in tourneys:
            for tlist in tourney.tourney_lists:
                ranking = TourneyRanking( tourney=tourney, player=tlist.player, rank=tlist.tourney_standing, elim_rank=tlist.tourney_elim_standing )
                self.pm.db_connector.get_session().add(ranking)
        self.pm.db_connector.get_session().commit()

    @unittest.skip("because")
    def testPortPlayerList(self):
        tourneys = self.pm.get_tourneys()
        for tourney in tourneys:
            for player in tourney.tourney_players:
                print "foo"

    #@unittest.skip("because")
    def testPortPlayerList(self):
        tourneys = self.pm.get_tourneys()
        for tourney in tourneys:
            for player in tourney.tourney_players:
                print "foo"



if __name__ == "__main__":
    if len (sys.argv) == 1:
        unittest.main()
