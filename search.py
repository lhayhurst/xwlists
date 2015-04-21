import unittest
from sqlalchemy import and_
from sqlalchemy.dialects import mysql
import myapp
from persistence import Match, Tourney, TourneyVenue, TourneyPlayer, TourneyList, Ship, ShipPilot, Pilot, ShipUpgrade, \
    Upgrade

def wildcard(term):
    return "*" + term + "*"

class Search:

    def __init__(self, tourney_name=None, locale_name=None, player_name=None, ship_name=None, pilot_name=None, upgrade_name=None):
        self.tourney_name = tourney_name
        self.locale_name = locale_name
        self.player_name = player_name
        self.ship_name = ship_name
        self.pilot_name = pilot_name
        self.upgrade_name = upgrade_name

    def search(self):

        myapp.db_connector.connect()
        session = myapp.db_connector.get_session()

        and_clauses = []
        if self.tourney_name is not None:
             and_clauses.append( Match([Tourney.tourney_name, Tourney.tourney_type], wildcard(self.tourney_name) ) )
        if self.locale_name is not None:
            and_clauses.append( Match([TourneyVenue.country, TourneyVenue.state, TourneyVenue.city, TourneyVenue.venue ], wildcard( self.locale_name ) ))
        if self.player_name is not None:
            and_clauses.append( Match([TourneyPlayer.player_name], wildcard( self.player_name ) ))
        if self.ship_name is not None:
            and_clauses.append( Match([ShipPilot.ship_type], wildcard( self.ship_name ) ) )
        if self.pilot_name is not None:
            and_clauses.append( Match([Pilot.name, Pilot.canon_name], wildcard(self.pilot_name) ))
        if self.upgrade_name is not None:
            and_clauses.append( Match([Upgrade.name, Upgrade.canon_name], wildcard(self.upgrade_name ) ) )


        match = session.query( Tourney, TourneyPlayer, TourneyList, Ship, ShipPilot, Pilot, ShipUpgrade, Upgrade).\
            join( TourneyVenue).\
            join( TourneyPlayer).\
            join( TourneyList).\
            join( Ship).\
            join( ShipPilot).\
            join( Pilot ).\
            outerjoin( ShipUpgrade).\
            outerjoin( Upgrade).\
            filter( and_( *and_clauses ) ).\
            statement.compile(dialect=mysql.dialect())

        connection = myapp.db_connector.get_engine().connect()
        ret = connection.execute(match)

        return ret



class SearchTest(unittest.TestCase):


    def testSearch(self):

        myapp.db_connector.connect()
        session = myapp.db_connector.get_session()

        mysearch = Search( tourney_name="world",  locale_name="roseville",
                           player_name="dom", ship_name="tie", pilot_name="soontir", upgrade_name="target")

        ret = mysearch.search()

        self.assertTrue( ret.rowcount == 1)
        result = [r[0] for r in ret]
        print result

if __name__ == "__main__":
    unittest.main()


