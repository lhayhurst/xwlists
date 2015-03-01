import json
import unittest
from requests import put, get

class apiTest(unittest.TestCase):

    def testGet(self):

        ids = get('http://localhost:5000/api/v1/tournament')
        print "got ids " + json.dumps(ids)
        return json.dump(ids)


if __name__ == "__main__":
    unittest.main()
