import unittest
import myapp
from persistence import PersistenceManager, TourneyList, ArchtypeList

__author__ = 'lhayhurst'

class ListUIDGen:

    def __init__(self, pm):
        self.pm = pm

    def generate(self):
        lists = self.pm.get_all_lists()
        i = 0
        hkeys = {}
        for list in lists:
            if list.archtype_list is not None and list.archtype_list.ships is not None:
                key = ArchtypeList.generate_hash_key(list.archtype_list.ships)
                if not hkeys.has_key(key):
                    hkeys[key] = [list]
                else:
                    hkeys[key].append(list)
                if i % 1000 == 0:
                    print "hashed %d records " % ( i )
                i = i + 1
        for key in hkeys:
            if len(hkeys[key]) > 1:
                #dupes!
                lists_to_fix = hkeys[key]
                #the first one gets to be the survivor
                survivor = lists_to_fix.pop()



class ListUIDTest(unittest.TestCase):
    def testGenerate(self):
        pm = PersistenceManager( myapp.db_connector )
        gen = ListUIDGen(pm)
        gen.generate()

if __name__ == "__main__":
    unittest.main()


