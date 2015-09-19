from sqlalchemy import BigInteger
import myapp
from persistence import PersistenceManager, ArchtypeList, Faction, Ship

__author__ = 'lhayhurst'

if __name__ == "__main__":

    pm = PersistenceManager( myapp.db_connector )
    ships = pm.db_connector.get_session().\
            query(Ship).all()

    for ship in ships:
        if ship.archtype_id is None:
            tlist = ship.tlist
            tlist.generate_hash_key()
            #get the archtype for this hashkey
            archtypes = pm.db_connector.get_session().query(ArchtypeList).\
                filter( ArchtypeList.hashkey == tlist.hashkey).all()

            archtype = None
            if archtypes is None or len(archtypes) == 0:
                #weird.  have to  create the archtype
                print "creating archtype"
                archtype = ArchtypeList()
                archtype.points = tlist.points
                archtype.faction = tlist.faction
                archtype.hashkey = tlist.hashkey
                ship.archtype = archtype
                pm.db_connector.get_session().add( archtype )
            else:
                archtype = archtypes[0]
                tlist.archtype_id = archtype.id
                ship.archtype_id = archtype.id
            pm.db_connector.get_session().add( tlist )
            pm.db_connector.get_session().add( ship )
    pm.db_connector.get_session().commit()


