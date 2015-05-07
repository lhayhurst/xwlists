import json
import unittest

ENTITIES = 'entities'

PARTICIPANT_ = 'Participant:#'

ENTITY_GROUP_MAP = "entityGroupMap"


class OrganizedPlayFormat:
    def __init__(self, data ):
        self.json_data = json.loads(data)

        if self.json_data is None:
            raise Exception("Unable to parse json data: " + data)


    def get_players(self):
        players_href = {}
        players_list = []
        players_href['players'] = players_list
        entities = self.json_data[ENTITY_GROUP_MAP][PARTICIPANT_][ENTITIES]
        for e in entities:
            first_name = e['first_name']
            last_name  = e['last_name']
            players_list.append( {"name" : "%s %s" % ( first_name, last_name )})
        return players_href


    def get_player_results(self):
        results = []



class OpFormatTest(unittest.TestCase):


    def testProcessFile(self):

        with self.assertRaises(Exception):
            OrganizedPlayFormat(None)

        f = open( "static/tourneys/op.json")
        data = f.read()

        opf = OrganizedPlayFormat(data)

        self.assertTrue( opf.json_data is not None )

        print opf.get_players()


if __name__ == "__main__":
    unittest.main()





