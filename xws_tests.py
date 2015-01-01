import json
import unittest
import sys
import urllib2

from bs4 import BeautifulSoup
from jsonschema import validate
from xwingmetadata import XWingMetaData


class XWSTests(unittest.TestCase):

    def testCanonize(self):
        meta = XWingMetaData()
        meta.canonicalize_ships_and_pilots()

    @unittest.skip("because")
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
        json_data = json.loads(code )
        print json_data

        #verify that everything matches up.  here are the rules:
        #Take the English-language name as printed on the card
        #Check for special case exceptions to these rules (see below)
        #Lowercase the name
        #Convert non-ASCII characters to closest ASCII equivalent (to remove umlauts, etc.)
        #Remove non-alphanumeric characters




if __name__ == "__main__":
    if len (sys.argv) == 1:
        unittest.main()