import json
import unittest
import sys
import urllib2

from bs4 import BeautifulSoup
from jsonschema import validate
from xwingmetadata import XWingMetaData


class XWSTests(unittest.TestCase):


    #@unittest.skip("because")
    def testGetUrl(self):

        response = urllib2.urlopen('http://xwing-builder.co.uk/xws/127470#view=full')
        html = response.read()
        soup = BeautifulSoup( html )
        full_code_div = soup.find(id= 'view_full')
        self.assertTrue( full_code_div is not None and len(full_code_div) > 0 )
        codes = full_code_div.find_all('code')
        self.assertEqual( len(codes) , 1 )
        code = codes[0].text
        self.assertTrue( code is not None )

        #pull in the schema
        # here        = os.path.dirname(__file__)
        # static_dir  = os.path.join( here, 'static' )
        # schema_file = os.path.join( static_dir, 'xwschema.json')

        #schema = json.loads(self.schema())
        xws = json.loads(code )
        print xws
        name = xws['name']
        faction = xws['faction']
        version = xws['version']
        points  = xws['points']
        pilots  = xws['pilots']

        for ship_pilot in xws['pilots']:
            ship = ship_pilot['ship']
            pilot = ship_pilot['name']
            ship_pilot_points = ship_pilot['points']
            upgrades = ship_pilot['upgrades']
            for upgrade_type in upgrades.keys():
                for upgrade in upgrades[upgrade_type]:
                    print "foo"











if __name__ == "__main__":
    if len (sys.argv) == 1:
        unittest.main()