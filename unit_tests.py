import os
from sqlalchemy import func
from myapp import db_connector
from persistence import PersistenceManager, Ship, Tourney, TourneyList
from rollup import Rollup

__author__ = 'lhayhurst'
import sys
import unittest


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):


        user     = os.environ['USER']
        password = os.environ['PASSWORD']
        sqlfile  = "./dbs/post_migration.sql"
        cmd = "/usr/local/mysql/bin/mysql -u %s -p%s 'sozin$lists' < %s" % ( user, password, sqlfile )

        print os.system(cmd)

        self.pm = PersistenceManager(db_connector)
        self.session = db_connector.get_session()



    def tearDown(self):

        self.session.close_all()


class TestIntegrity(DatabaseTestCase):

    @unittest.skip("because")
    def testTListCreation(self):
        self.pm.db_connector.get_base().metadata.create_all(self.pm.db_connector.get_engine(), checkfirst=True )

        self.pm.db_connector.get_session().commit()


    @unittest.skip("because")
    def testDeleteTourney(self):
        tourneys = self.pm.get_tourneys().all()
        self.assertEqual( 2, len(tourneys))
        tname = tourneys[0].tourney_name
        self.pm.delete_tourney( tname )
        tourneys = self.pm.get_tourneys().all()
        self.assertEqual( 1, len(tourneys))
        self.assertTrue(not  tname == tourneys[0].tourney_name )

    def get_num_ships(self, tourney):
        return self.pm.db_connector.get_session().\
        query( func.count(Ship.id).label("num_ships" ) ).\
        filter(Tourney.id == tourney.id ).first()[0]


    @unittest.skip("because")
    def testDeleteTourneyList(self):
        tname = 'Worlds 2014 Flight One'
        tourney = self.pm.get_tourney( tname )

        num_lists = len(tourney.tourney_lists)

        first_tourney_list   = tourney.tourney_lists[ 0 ]
        num_ships_in_tourney = self.get_num_ships( tourney )
        self.assertTrue(num_ships_in_tourney > 0 )
        num_ships_in_list = len( first_tourney_list.ships )
        self.assertTrue( first_tourney_list.faction is not None )
        self.assertTrue( first_tourney_list.points is not None )
        self.assertTrue( first_tourney_list.ships is not None )
        self.assertTrue( len(first_tourney_list.ships) >  0 )

        self.pm.delete_tourney_list_details( first_tourney_list )

        tourney = self.pm.get_tourney( tname )
        self.assertTrue( num_lists == len(tourney.tourney_lists ))
        first_tourney_list = tourney.tourney_lists[0]
        num_ships_after_delete = self.get_num_ships( first_tourney_list )
        self.assertEqual( num_ships_in_tourney - num_ships_in_list, num_ships_after_delete )


    @unittest.skip("because")
    def testGetRandomTourneyList(self):
        tname = 'Worlds 2014 Flight One'
        tourney = self.pm.get_tourney( tname )

        #this method returns a random tourney list that has yet to be populated
        #in the default state, everything is populated, so it should return none
        random_tourney_list = self.pm.get_random_tourney_list( tourney )
        assert( random_tourney_list is None )

        #now delete some tourney list details.
        first_tourney_list = tourney.tourney_lists[0]
        first_tourney_list_id = first_tourney_list.id
        self.pm.delete_tourney_list_details( first_tourney_list)

        #and get a random one again.  it should return the one whose details we detailed
        random_tourney_list = self.pm.get_random_tourney_list( tourney )
        assert( random_tourney_list is not None )
        self.assertEqual( random_tourney_list.id, first_tourney_list_id )


    @unittest.skip("because")
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
            print ("total points %d") % ( total_points )


    def testRollup(self):

        r = Rollup( self.pm )
        data = r.rollup_by_ship_faction(use_counts=False)
        self.assertTrue( data is not None )
        self.assertEqual( len(data), 2 )

        rebs = data[0]
        self.assertEqual( rebs['drilldown']['name'], 'Rebel')



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
