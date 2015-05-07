import re
import unittest

from sqlalchemy import and_, or_, func
from whoosh.qparser import QueryParser
from whoosh.query import Term

import myapp
from persistence import TourneyList, Ship, ShipPilot, Pilot, ShipUpgrade, \
    Upgrade, PersistenceManager, Tourney, TourneyVenue


def wildcard(term):
    return term


expression_map = { 'AND' : and_,
                   'and' : and_,
                   'or'  : or_,
                   'OR'  : or_ }

PILOT_MATCH = "pilot_match"
SHIP_MATCH  = "ship_match"
UPGRADE_MATCH = "upgrade_match"
COUNTRY_MATCH = "country_match"
STATE_MATCH   = "state_match"
CITY_MATCH    = "city_match"
VENUE_MATCH   = "venue_match"
TOURNEY_TYPE  = "tourney_type"

term_type_map = { "p": PILOT_MATCH,
                  "pilot": PILOT_MATCH,
                  "s" : SHIP_MATCH,
                  "ship" : SHIP_MATCH,
                  "u" : UPGRADE_MATCH,
                  "upgrade" : UPGRADE_MATCH,
                  "country" : COUNTRY_MATCH,
                  "state" : STATE_MATCH,
                  "city" : CITY_MATCH,
                  "venue" : VENUE_MATCH,
                  "type" : TOURNEY_TYPE
                }

def tree_to_expr(tree, subq):
    if isinstance(tree, Term):
        term = str(tree.text)
        term_type, term_value = term.split("=")
        match_expr = term_type_map[ term_type ]
        if match_expr == PILOT_MATCH:
            return subq.c.pilot_name.like( '%' + term_value + '%')
        elif match_expr == SHIP_MATCH:
            return subq.c.ship_name.like( '%' + term_value + '%')
        elif match_expr == UPGRADE_MATCH:
            return subq.c.upgrade_name.like( '%' + term_value + '%')
        elif match_expr == COUNTRY_MATCH:
            return subq.c.country_name.like( '%' + term_value + '%')
        elif match_expr == STATE_MATCH:
            return subq.c.state_name.like( '%' + term_value + '%')
        elif match_expr == CITY_MATCH:
            return subq.c.city_name.like( '%' + term_value + '%')
        elif match_expr == VENUE_MATCH:
            return subq.c.venue_name.like( '%' + term_value + '%')
        elif match_expr == TOURNEY_TYPE:
            return subq.c.tourney_type.like( '%' + term_value + '%')

    fn = expression_map[tree.JOINT.strip()]
    return fn(
        *(
            [tree_to_expr( child, subq) for child in tree ]
        )
    )

kvpair = re.compile( r'^(s=.+)|(ship=.+)|(p=.+)|(pilot=.+)|(u=.+)|(country=.+)|(state=.+)|(city=.+)|(venue=.+)|(type=.+)')

class Search:

    def is_valid_term(self, q):
        if isinstance(q, Term):
            term = str(q.text)
            m    = kvpair.match( term )
            if m is None:
                return False
            else:
                return True
        else:
            return True

    def validate_search_term(self, q):
        if not self.is_valid_term(q):
            return "Invalid search query: "

        if len(q.all_terms()) > 1:
            for i in q:
                if not self.is_valid_term(i):
                    return "Invalid search query: "

        return None

    def __init__(self, search_term):

        parser = QueryParser("content", schema=None)
        q = parser.parse(search_term)
        invalid = self.validate_search_term(q)
        if invalid:
            raise ValueError(invalid + search_term)

        myapp.db_connector.connect()
        session = myapp.db_connector.get_session()

        subq = session.query( TourneyList.id.label("tourney_list_id"),
                              TourneyVenue.country.label("country_name"),
                              TourneyVenue.state.label("state_name"),
                              TourneyVenue.city.label("city_name"),
                              TourneyVenue.venue.label("venue_name"),
                              Tourney.tourney_type.label("tourney_type"),
                              func.group_concat( ShipPilot.ship_type.distinct()).label("ship_name" ),
                              func.group_concat( func.concat( Pilot.name, " ", Pilot.canon_name )).label("pilot_name"),
                              func.group_concat( func.concat( Upgrade.name, " ", Upgrade.canon_name ) ).label("upgrade_name") ). \
            join(Tourney).\
            join(TourneyVenue).\
            join(Ship). \
            join(ShipPilot). \
            join(Pilot). \
            outerjoin(ShipUpgrade). \
            outerjoin(Upgrade).\
            group_by( TourneyList.id).subquery()


        fn  = tree_to_expr(q, subq)
        self.query = session.query(subq.c.tourney_list_id).filter( fn )



# select * from ( SELECT tourney_list.id AS tourney_list_id ,
# GROUP_CONCAT(distinct ship_pilot.ship_type  SEPARATOR ' ' ) as ship,
# GROUP_CONCAT(distinct CONCAT( pilot.name, ' ',  pilot.canon_name)  SEPARATOR ' ' ) as pilot1,
# GROUP_CONCAT(distinct CONCAT( upgrade.name, ' ',  upgrade.canon_name)  SEPARATOR ' ' ) as uprade
#  FROM tourney_list
# INNER JOIN ship ON tourney_list.id = ship.tlist_id
# INNER JOIN ship_pilot ON ship_pilot.id = ship.ship_pilot_id
# INNER JOIN pilot ON pilot.id = ship_pilot.pilot_id
# LEFT OUTER JOIN ship_upgrade ON ship.id = ship_upgrade.ship_id
# LEFT OUTER JOIN upgrade ON upgrade.id = ship_upgrade.upgrade_id
# group by tourney_list.id ) as rr
# WHERE  rr.pilot1 like '%Dash%' and rr.pilot1 like '%Chew%'

    def search(self):

        ret = []
        seen = {}
        pm = PersistenceManager( myapp.db_connector )

        for rec in self.query:
             list_id = rec[0]
             if not seen.has_key( list_id ):
                 list    = pm.get_tourney_list( list_id )
                 seen[list_id] = 1
                 ret.append( list )

        return ret



class SearchTest(unittest.TestCase):


    def testSearch(self):

        with self.assertRaises(ValueError):
            Search("foo")

        with self.assertRaises(ValueError):
            Search("a=bar")

        with self.assertRaises(ValueError):
            Search("=bar")

        with self.assertRaises(ValueError):
            Search("s=")

        with self.assertRaises(ValueError):
            Search("s=bar and s=baz")


if __name__ == "__main__":
    unittest.main()


