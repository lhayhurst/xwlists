import os
from sqlalchemy import func
from cryodex import Cryodex
from myapp import db_connector
from persistence import PersistenceManager, Ship, Tourney, TourneyList, TourneyRound, RoundResult, TourneyRanking, \
    TourneyPlayer, Set, TourneySet
from rollup import Rollup
import xwingmetadata

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
    def testApplySetToTourney(self):
        sets = self.pm.db_connector.get_session().query(Set)
        tourneys = self.pm.get_tourneys()
        for tourney in tourneys:
            for set in sets:
                if set.set_name != 'Wave 5':
                    ts = TourneySet( tourney_id=tourney.id, set_id=set.id)
                    self.pm.db_connector.get_session().add(ts)
        self.pm.db_connector.get_session().commit()

    @unittest.skip("because")
    def testCreateSetTable(self):
        for set in xwingmetadata.sets_and_expansions.keys():
            s = Set( set_name=set )
            self.pm.db_connector.get_session().add(s)
        self.pm.db_connector.get_session().commit()

    @unittest.skip("because")
    def testPortPlayerTable(self):
        tourneys = self.pm.get_tourneys()
        for tourney in tourneys:
            for tlist in tourney.tourney_lists:
                ranking = TourneyRanking( tourney=tourney, player=tlist.player, rank=tlist.tourney_standing, elim_rank=tlist.tourney_elim_standing )
                self.pm.db_connector.get_session().add(ranking)
        self.pm.db_connector.get_session().commit()




if __name__ == "__main__":
    if len (sys.argv) == 1:
        unittest.main()
