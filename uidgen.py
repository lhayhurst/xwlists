import unittest
import myapp
from persistence import PersistenceManager

__author__ = 'lhayhurst'

class ListUIDGen:

    def __init__(self, pm):
        self.pm = pm

    def generate(self):
        lists = self.pm.get_all_lists()
        i = 0
        listhref = {}
        for list in lists:
            list.generate_hash_key()
            if i % 1000 == 0:
                print "committing %d records " % ( i )
                self.pm.db_connector.get_session().commit()
            i = i + 1

class ListUIDTest(unittest.TestCase):
    def testGenerate(self):
        pm = PersistenceManager( myapp.db_connector )
        gen = ListUIDGen(pm)
        gen.generate()

if __name__ == "__main__":
    unittest.main()


