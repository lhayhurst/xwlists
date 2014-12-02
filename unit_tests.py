from myapp import db_connector
from persistence import PersistenceManager, TourneyList

__author__ = 'lhayhurst'
import sys
import unittest


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.pm = PersistenceManager(db_connector)
        self.session = db_connector.get_session()


    def tearDown(self):

        self.session.close_all()


class TestIntegrity(DatabaseTestCase):

    @unittest.skip("because")
    def testTListCreation(self):
        self.pm.db_connector.get_base().metadata.create_all(self.pm.db_connector.get_engine(), checkfirst=True )

        self.pm.db_connector.get_session().commit()

    # @unittest.skip("because")
    # def testPopulateNewTables(self):
    #     tourneys = self.pm.get_tourneys()
    #
    #     self.assertTrue(tourneys)
    #     self.assertTrue(len(tourneys.all()) == 2)
    #
    #     newt = []
    #     for tourney in tourneys:
    #         tourney2 = Tourney2( tourney_name=tourney.tourney_name, tourney_date=tourney.tourney_date, tourney_type=tourney.tourney_type )
    #         newt.append( tourney2 )
    #
    #
    #         for tl in tourney.tourney_lists:
    #              tl2 = TourneyList( player_name = tl.player_name,
    #                           tourney_standing = tl.tourney_standing,
    #                           tourney_elim_standing = tl.tourney_elim_standing,
    #                           image = tl.image,
    #                           faction = tl.list.faction,
    #                           points = tl.list.points,
    #                           tourney=tourney2)
    #              tourney2.tlists.append(tl2)
    #              list = tl.list
    #              for ship in list.ships:
    #                  ship2 = Ship2( ship_pilot_id=ship.ship_pilot.id, tlist=tl2)
    #                  tl2.ships.append(ship2)
    #                  upgrades = ship.upgrades
    #                  if upgrades is not None:
    #                      for ship_upgrade in upgrades:
    #                         su2 = ShipUpgrade2( upgrade=ship_upgrade.upgrade, ship2=ship2 )
    #                         ship2.upgrades.append( su2 )
    #
    #     db_connector.get_session().add_all( newt )
    #     db_connector.get_session().commit()

    #@unittest.skip("because")
    def testNewTourneyList(self):
        tourneys = self.pm.get_tourneys()

        self.assertTrue(tourneys)
        self.assertTrue(len(tourneys.all()) == 2)

        for tourney in tourneys:
            num_tlists   = len(tourney.tourney_lists)
            total_points = 0

            for tl in tourney.tourney_lists:
                num_list_points   = 0
                self.assertTrue( tl.faction is not None )
                self.assertTrue(len(tl.ships) > 0)
                self.assertTrue( tl.image is not None )
                self.assertTrue( tl.tourney_elim_standing is None )
                self.assertTrue( tl.tourney_standing > 0 )
                self.assertTrue( tl.points > 0 )
                for ship in tl.ships:
                    sp = ship.ship_pilot
                    self.assertTrue( sp is not None )
                    pilot = sp.pilot
                    self.assertTrue( pilot is not None)
                    num_list_points = num_list_points + pilot.cost
                    upgrades = ship.upgrades
                    if upgrades is not None:
                        for ship_upgrade in upgrades:
                            upgrade = ship_upgrade.upgrade
                            self.assertTrue( upgrade is not None)
                            self.assertEquals( ship, ship_upgrade.ship)
                            self.assertTrue( upgrade.cost is not None)
                            self.assertTrue( upgrade.cost >= -2)
                            num_list_points = num_list_points + upgrade.cost
                self.assertTrue( num_list_points <= 100 )
                if num_list_points != tl.points:
                    print ("list %s has recorded points %d and calculated points %d" % ( tl.id, tl.points, num_list_points ) )
                total_points = total_points + num_list_points
            self.assertTrue( total_points <= num_tlists * 100 )

    @unittest.skip("because")
    def testTourneyList(self):
        tourneys = self.pm.get_tourneys()

        self.assertTrue(tourneys)
        self.assertTrue(len(tourneys.all()) == 2)

        for tourney in tourneys:
            num_tlists   = len(tourney.tourney_lists)
            total_points = 0

            for tl in tourney.tourney_lists:
                num_list_points   = 0

                list = tl.list
                self.assertTrue( list.faction is not None )
                self.assertTrue(len(list.ships) > 0)
                for ship in list.ships:
                    sp = ship.ship_pilot
                    self.assertTrue( sp is not None )
                    pilot = sp.pilot
                    self.assertTrue( pilot is not None)
                    num_list_points = num_list_points + pilot.cost
                    upgrades = ship.upgrades
                    if upgrades is not None:
                        for ship_upgrade in upgrades:
                            upgrade = ship_upgrade.upgrade
                            self.assertTrue( upgrade is not None)
                            self.assertEquals( ship, ship_upgrade.ship)
                            self.assertTrue( upgrade.cost is not None)
                            self.assertTrue( upgrade.cost >= -2)
                            num_list_points = num_list_points + upgrade.cost
                self.assertTrue( num_list_points <= 100 )
                total_points = total_points + num_list_points
            self.assertTrue( total_points <= num_tlists * 100 )

if __name__ == "__main__":
    if len (sys.argv) == 1:
        unittest.main()
