from sqlalchemy import BigInteger
import myapp
from persistence import PersistenceManager, ArchtypeList, Faction

__author__ = 'lhayhurst'

if __name__ == "__main__":

    archtypes_hash = {}

    pm = PersistenceManager( myapp.db_connector )
    hashkeys = pm.get_all_hashkeys()
    for hashkey in hashkeys:
        lists = pm.get_lists_for_hashkey(hashkey[0])
        for list in lists:
            if not archtypes_hash.has_key( hashkey[0]):
                a = ArchtypeList()
                if list.faction is not None:
                    a.hashkey = hashkey[0]
                    a.faction = list.faction
                    if list.points is not None:
                        a.points = list.points
                    pm.db_connector.get_session().add( a )
                    archtypes_hash[hashkey[0]] = a
    pm.db_connector.get_session().commit()


#143,rebel, 100