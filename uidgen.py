import unittest
import myapp
from persistence import PersistenceManager, TourneyList, ArchtypeList

__author__ = 'lhayhurst'

class ListUIDGen:

    def __init__(self, pm):
        self.pm = pm

    def regenerate_archtype_keys(self):
        archtypes = self.pm.get_all_archtypes()
        i = 0
        for a in archtypes:
            if a.ships is None or len(a.ships) is 0:
                self.pm.db_connector.get_session().delete(a)
                continue
            hashkey   = a.generate_hash_key(a.ships)
            if hashkey is None or hashkey is 0: #some cleanup here ...
                self.pm.db_connector.get_session().delete(a)
            else:
                a.hashkey = hashkey
                if i % 500 == 0:
                    print "hashed %d archtypes " % ( i )
                i = i + 1

    def fix_dupes(self): #update ship set ship_pilot_id=195 where ship_pilot_id=196
        goners  = {}
        keepers = {}
        self.regenerate_archtype_keys()
        self.pm.db_connector.get_session().commit()
        self.fix_online_dupes(keepers, goners)
        self.pm.db_connector.get_session().commit()
        self.fix_otb_dupes(keepers, goners)

        print ("deleting %d archtypes" % ( len( goners.values() )))
        print ("keeping %d archtypes" % len(keepers.values()))
        for archtype in goners.values():
            self.pm.db_connector.get_session().delete(archtype)
        self.pm.db_connector.get_session().commit()

        self.cleanup_unused_archtypes()

    def cleanup_unused_archtypes(self):
        i = 0
        archtypes = self.pm.get_all_archtypes()
        num_archtypes = len(archtypes)
        num_deletes = 0
        for a in archtypes:
            if len(a.tourney_lists) == 0 and len(a.p1_league_lists) == 0 and len(a.p2_league_lists) == 0:
                self.pm.db_connector.get_session().delete(a)
                num_deletes = num_deletes + 1
            if i % 1000 == 0:
                print ("checked %d archtype dupes" % (i))
            i = i + 1
        print("deleting %d archtypes from total count of %d" % (num_deletes, num_archtypes))
        self.pm.db_connector.get_session().commit()

    def process_list(self, list, keepers, goners):
        if list.archtype_list is not None and list.archtype_list.ships is not None:
            key = list.archtype_list.hashkey
            if not keepers.has_key(key):
                keepers[key] = list.archtype_list
            else:
                proto_list = keepers[key]
                if proto_list.id != list.archtype_list.id:
                    goners[list.archtype_list.id] = list.archtype_list
                list.archtype_list_id = proto_list.id

    def process_match_list(self, archtype_list, keepers, goners):
        if archtype_list is not None and archtype_list.ships is not None:
            key = archtype_list.hashkey
            if not keepers.has_key(key):
                keepers[key] = archtype_list
                return archtype_list
            else:
                proto_list = keepers[key]
                if proto_list.id != archtype_list.id:
                    goners[archtype_list.id] = archtype_list
                return proto_list

    def fix_online_dupes(self,keepers, goners):
        matches = self.pm.get_all_league_matches()
        i = 0

        for match in matches:
            list1 = match.player1_list
            list2 = match.player2_list
            if list1 is not None:
                new_p1_list = self.process_match_list(list1,keepers,goners)
                match.player1_list_id = new_p1_list.id

            if list2 is not None:
                new_p2_list = self.process_match_list(list2,keepers,goners)
                match.player2_list_id = new_p2_list.id

            if i % 1000 == 0:
                print "hashed %d vassal matches " % ( i )
            i = i + 1

    def fix_otb_dupes(self,keepers, goners):
        lists = self.pm.get_all_lists()
        i = 0
        for list in lists:
            self.process_list(list,keepers,goners)
            if i % 1000 == 0:
                print "hashed %d otb records " % ( i )
            i = i + 1
        self.pm.db_connector.get_session().commit()




class ListUIDTest(unittest.TestCase):
    def testGenerate(self):
        pm = PersistenceManager( myapp.db_connector )
        gen = ListUIDGen(pm)
        gen.fix_dupes()

if __name__ == "__main__":
    unittest.main()


