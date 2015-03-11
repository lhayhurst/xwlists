import json
import unittest
from requests import put, get, post
import myapp
from persistence import PersistenceManager




class apiTest(unittest.TestCase):
    def testGetTournaments(self):
        resp = get('http://localhost:5000/api/v1/tournaments')
        ids = resp.json()
        self.assertTrue(ids is not None)
        self.assertTrue(len(ids) > 0)

    def testPutTournament(self):
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30,
                            'venue':
                                {'country': 'United States', 'state': 'Illinois', 'city': 'Chicago',
                                 'venue': 'Dice Dojo'
                                },
                            'players': [
                                {
                                    "name": "Lyle Hayhurst",
                                    "mov": 622,
                                    "score": 20,
                                    "sos": 50,
                                    'dropped': False,
                                    "rank": {
                                        "swiss": 1,
                                        "elimination": 2
                                    }
                                },
                                {
                                    "name": "Brandon Prokos",
                                    "mov": 647,
                                    "score": 15,
                                    "sos": 45,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 2,
                                        "elimination": 4
                                    }
                                }
                            ]
        }
        }

        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(201, resp.status_code)
        js = resp.json()
        self.assertTrue(js.has_key('tournament'))
        js = js['tournament']
        self.assertTrue(js.has_key('name'))
        self.assertTrue(js.has_key('id'))
        self.assertTrue(js['name'] == 'foobar')

        # look it up in the db and verify that stuff matched out ok
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(int(js['id']))
        self.assertTrue(tourney is not None)
        self.assertEqual(tourney.tourney_name, 'foobar')
        self.assertEqual(str(tourney.tourney_date), '2015-05-25')
        self.assertEqual(tourney.tourney_type, "Store Championship")
        self.assertEqual(tourney.round_length, 60)
        self.assertEqual(tourney.participant_count, 30)
        self.assertEqual(tourney.venue.country, 'United States')
        self.assertEqual(tourney.venue.state, 'Illinois')
        self.assertEqual(tourney.venue.city, 'Chicago')
        self.assertEqual(tourney.venue.venue, 'Dice Dojo')

        #and the players/rankings
        self.assertEqual(len(tourney.tourney_players), 2)
        p1 = tourney.tourney_players[0]
        self.assertEqual('Lyle Hayhurst', p1.player_name)

    # tests various error conditions
    def testPutTournamentBad(self):
        #no data payload
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=None)
        self.assertEqual(404, resp.status_code)

        #empty data payload
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps({}))
        self.assertEqual(404, resp.status_code)

        #no tournament fields
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps({"tournament": {}}))
        self.assertEqual(404, resp.status_code)

        #missing required fields 1
        t = {"tournament": {"name": "foobar"}}
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(404, resp.status_code)

        #missing required fields 2
        t = {"tournament": {"name": "foobar", "date": "2015-05-25"}}
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(404, resp.status_code)

        #missing required fields 3
        t = {"tournament": {"name": "foobar", "date": "2015-05-25", "type": "Store Championship"}}
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(404, resp.status_code)

        #missing required fields 4
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60}}
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(404, resp.status_code)

        #invalidly formatted date
        t = {"tournament": {"name": "foobar", "date": "foobar",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30}}
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(404, resp.status_code)

        #invalidly formatted type
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Smore Championship", "round_length": 60, "participant_count": 30}}
        resp = post('http://localhost:5000/api/v1/tournaments',
                    data=json.dumps(t))
        self.assertEqual(404, resp.status_code)


if __name__ == "__main__":
    unittest.main()
