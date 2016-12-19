from myapp import db_connector
import myapp
from persistence import PersistenceManager, UpgradeType, Upgrade
from xwingmetadata import XWingMetaData
from xws import XWSToJuggler

__author__ = 'lhayhurst'
import sys
import unittest


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.session = db_connector.get_session()
        self.pm  = PersistenceManager(myapp.db_connector)


    def tearDown(self):
        self.session.close_all()


class TestPersistence(DatabaseTestCase):

    #@unittest.skip("because")
    def testTrue(self):
        self.assertTrue(True)

    def testArchtypeHashkeyGeneration(self):
        corran = {
            "name": "corranhorn",
            "points": 46,
            "ship": "ewing",
            "upgrades": {"ept": ["veteraninstincts"], "system": ["firecontrolsystem"], "amd": ["r2d2"],
                         "mod": ["engineupgrade"]}
        }
        dash = {
            "name": "dashrendar",
            "points": 54,
            "ship": "yt2400freighter",
            "upgrades": {"ept": ["pushthelimit"], "cannon": ["heavylasercannon"], "crew": ["kananjarrus"],
                         "title": ["outrider"]}
        }
        xws1 = {"faction": "rebel", "name": "Corran46 Dash 54",
                "pilots": [corran, dash],
                "points": 100,
                "vendor": {
                    "yasb": {
                        "builder": "(Yet Another) X-Wing Miniatures Squad Builder",
                        "builder_url": "https://geordanr.github.io/xwing/",
                        "link": "https://geordanr.github.io/xwing/?f=Rebel%20Alliance&d=v4!s!75:27,36,-1,3:-1:3:;95:18,23,-1,159:14:-1:&sn=Unnamed%20Squadron"
                    }
                },
                "version": "0.3.0"
                }
        xws2 = {"faction": "rebel", "name": "Corran46 Dash 54",
                "pilots": [dash, corran],
                "points": 100,
                "vendor": {
                    "yasb": {
                        "builder": "(Yet Another) X-Wing Miniatures Squad Builder",
                        "builder_url": "https://geordanr.github.io/xwing/",
                        "link": "https://geordanr.github.io/xwing/?f=Rebel%20Alliance&d=v4!s!75:27,36,-1,3:-1:3:;95:18,23,-1,159:14:-1:&sn=Unnamed%20Squadron"
                    }
                },
                "version": "0.3.0"
                }

        converter = XWSToJuggler(xws1)
        archtype1, first_time_archtype_seen1 = converter.convert(self.pm)

        converter = XWSToJuggler(xws2)
        archtype2, first_time_archtype_seen2 = converter.convert(self.pm)

        print(archtype1.hashkey)
        print(archtype2.hashkey)
        self.assertTrue(archtype1.hashkey == archtype2.hashkey)


if __name__ == "__main__":
    unittest.main()
