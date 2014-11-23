from myapp import db_connector
import myapp
from persistence import PersistenceManager

__author__ = 'lhayhurst'
import sys
import unittest


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.persistence_manager = PersistenceManager(True)

        #just keep a top level reference to these guys for ease of use
        self.session = db_connector.get_session()

        #and then create the database schema, reference tables
        self.persistence_manager.create_schema()
        self.persistence_manager.populate_reference_tables()
        self.session.commit()

    def tearDown(self):

#        self.session.flush()
        self.session.close_all()
        self.persistence_manager.drop_schema()


class TestPersistence(DatabaseTestCase):

    #@unittest.skip("because")
    def testSchemaConstruction(self):
        self.assertTrue(True)



if __name__ == "__main__":
    if len (sys.argv) == 1:
        unittest.main()
    elif sys.argv[1] == 'create':
        pm = PersistenceManager(db_connector)
        pm.create_schema()
        pm.populate_reference_tables()
        db_connector.get_session().commit()
        db_connector.get_session().close_all()
    elif sys.argv[1] == 'destroy':
        pm = PersistenceManager(db_connector)
        pm.drop_schema()
        db_connector.get_session().commit()
        db_connector.get_session().close_all()