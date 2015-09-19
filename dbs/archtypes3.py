from sqlalchemy import BigInteger
import myapp
from persistence import PersistenceManager, ArchtypeList, Faction, Ship

#this script removes duplicate ships so that the mapping from ship to archtype is 1-1

__author__ = 'lhayhurst'

if __name__ == "__main__":

    pm = PersistenceManager( myapp.db_connector )
    ships = pm.db_connector.get_session().query(Ship).all()
    goners = {}
    for s in ships:
        archtype_id = s.archtype_id
        list_id     = s.tlist_id
        if not goners.has_key( archtype_id):
            list_ids = {}
            list_ids[list_id] = [ s ]
            goners[ archtype_id] = list_ids
        else:
            list_ids = goners[archtype_id]
            if not list_ids.has_key( s.tlist_id):
                list_ids[list_id] = [s]
            else:
                list_ids[ list_id  ].append( s )
    #now go through and crush all but one of this for an archtype, tlist pair
    for archtype_id in goners.keys():
        tlists = goners[archtype_id].keys()
        if len(tlists) > 0:
            iterships = iter(tlists)
            next(iterships)
            for tlist_id in iterships:
                ships = goners[archtype_id][tlist_id]
                for ship in ships:
                    pm.db_connector.get_session().delete( ship )

    pm.db_connector.get_session().commit()





