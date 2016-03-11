import unittest
import myapp
from persistence import PersistenceManager, TourneyList, ArchtypeList

__author__ = 'lhayhurst'

class ListUIDGen:

    def __init__(self, pm):
        self.pm = pm

    def fix_dupes(self):
        lists = self.pm.get_all_lists()
        i = 0
        hkeys = {}
        goners = {}
        for list in lists:
            if list.archtype_list is not None and list.archtype_list.ships is not None:
                key = ArchtypeList.generate_hash_key(list.archtype_list.ships)
                if not hkeys.has_key(key):
                    hkeys[key] = list
                else:
                    #fix it
                    proto_list = hkeys[key]

                    #get the matches for this guy
                    matches = self.pm.get_matches_for_archtype(list.archtype_list.id)
                    for match in matches:
                        if match.player1_list_id == list.archtype_list.id:
                            match.player1_list_id = proto_list.archtype_list.id
                            match.player1_list    = proto_list.archtype_list
                        if match.player2_list_id == list.archtype_list.id: #could be a mirror match
                            match.player2_list_id = proto_list.archtype_list.id
                            match.player2_list    = proto_list.archtype_list

                        self.pm.db_connector.get_session().add(match)

                    #and then update the actual list.
                    list.archtype_list = proto_list.archtype_list


                    self.pm.db_connector.get_session().add(list)
                    goners[list.archtype_list.id] = list.archtype_list
                if i % 1000 == 0:
                    print "hashed %d records " % ( i )
                i = i + 1
        #here we go
        self.pm.db_connector.get_session().commit()

        #for archtype in goners.values():
            #get the matches for this list and update them
            #how the heck are these duplicates sneaking in?
            #self.pm.db_connector.get_session().delete(archtype)

        #self.pm.db_connector.get_session().commit()





class ListUIDTest(unittest.TestCase):
    def testGenerate(self):
        pm = PersistenceManager( myapp.db_connector )
        gen = ListUIDGen(pm)
        gen.fix_dupes()

if __name__ == "__main__":
    unittest.main()


