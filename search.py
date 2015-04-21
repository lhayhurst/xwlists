import unittest
from sqlalchemy import select, or_, and_
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import aliased
import myapp
from persistence import Match, Tourney, TourneyVenue, TourneyPlayer, TourneyList, Ship, ShipPilot, Pilot, ShipUpgrade, \
    Upgrade

def wildcard(term):
    return "*" + term + "*"

class SearchTest(unittest.TestCase):


    def testSearch(self):

        myapp.db_connector.connect()
        session = myapp.db_connector.get_session()

        tourney = "world"
        city    = "roseville"
        player  = "dom"
        ship    = "tie"
        pilot   = "soontir"

        match = session.query( Tourney, TourneyList, TourneyPlayer, Ship, ShipPilot, Pilot, ShipUpgrade, Upgrade ).\
            join( Tourney, TourneyVenue).\
            join( Tourney, TourneyPlayer).\
            join( Tourney, TourneyList).\
            join( TourneyPlayer, TourneyList ).\
            join( Ship, TourneyList ).\
            join( ShipPilot, Ship ).\
            join( Pilot, ShipPilot ).\
            outerjoin( ShipUpgrade, Ship).\
            outerjoin( Upgrade, ShipUpgrade).\
            filter( and_(
                         Match([Tourney.tourney_name, Tourney.tourney_type], wildcard(tourney) ),
                         Match([TourneyVenue.country, TourneyVenue.state, TourneyVenue.city, TourneyVenue.venue ], wildcard( city ) ),
                         Match([TourneyPlayer.player_name], wildcard( player ) ),
                         Match([ShipPilot.ship_type], wildcard( ship ) ),
                         Match([Pilot.name, Pilot.canon_name], wildcard(pilot) ),
                   ) ).\
            statement.compile(dialect=mysql.dialect())

        connection = myapp.db_connector.get_engine().connect()
        ret = connection.execute(match)
        for row in ret:
            print row


if __name__ == "__main__":
    unittest.main()


