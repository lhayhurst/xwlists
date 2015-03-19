import json
import unittest
from requests import put, get, post, delete
import myapp
from persistence import PersistenceManager


dev_url  =  'http://localhost:5000/api/v1/tournaments'
prod_url = 'http://lists.starwarsclubhouse.com/api/v1/tournaments'

class apiTest(unittest.TestCase):
    def testGetTournaments(self):
        resp = get(dev_url)
        ids = resp.json()
        self.assertTrue(ids is not None)
        self.assertTrue(len(ids) > 0)

    def testPutAndDeleteTournament(self):
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30,
                            'venue':
                                {'country': 'United States', 'state': 'Illinois', 'city': 'Chicago',
                                 'venue': 'Dice Dojo'
                                },
                            'sets_used': ["Core Set", "Wave 1", "Wave 2", "Wave 3",
                                          "Wave 4", "Wave 5", "Wave 6",
                                          "GR-75 Expansion", "CR90 Expansion",
                                          "Imperial Aces Expansion",
                                          "Rebel Aces Expansion"

                            ],
                            'format': 'Standard - 100 Point Dogfight',
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
                                    "name": "Matt Babiash",
                                    "mov": 647,
                                    "score": 15,
                                    "sos": 45,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 2,
                                        "elimination": 4
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
                                },
                                {
                                    "name": "Phil Kalata",
                                    "mov": 647,
                                    "score": 15,
                                    "sos": 45,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 2,
                                        "elimination": 4
                                    }
                                },
                                {
                                    "name": "Zach Carriger",
                                    "mov": 647,
                                    "score": 15,
                                    "sos": 45,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 2,
                                        "elimination": 4
                                    }
                                },
                                {
                                    "name": "David Pontier",
                                    "mov": 647,
                                    "score": 15,
                                    "sos": 45,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 2,
                                        "elimination": 4
                                    }
                                },
                            ],
                            "rounds": [
                                {
                                    "round-type": "swiss",
                                    "round-number": 1,
                                    "matches": [
                                        {
                                            "player1": "Lyle Hayhurst",
                                            "player1points": 100,
                                            "player2": "Brandon Prokos",
                                            "player2points": 48,
                                            "result": "win"
                                        },
                                        {
                                            "player1": "Zach Carriger",
                                            "player1points": 32,
                                            "player2": "Phil Kalata",
                                            "player2points": 0,
                                            "result": "win"
                                        }
                                    ]
                                },
                                {
                                    "round-type": "elimination",
                                    "round-number": 4,
                                    "matches": [
                                        {
                                            "player1": "Lyle Hayhurst",
                                            "player1points": 100,
                                            "player2": "Matt Babiash",
                                            "player2points": 80,
                                            "result": "win"
                                        },
                                        {
                                            "player1": "Phil Kalata",
                                            "player1points": 0,
                                            "player2": "David Pontier",
                                            "player2points": 100,
                                            "result": "win"
                                        }
                                    ]
                                }
                            ]

                }
        }


        resp = post(dev_url,
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
        self.assertEqual(tourney.format, 'Standard - 100 Point Dogfight')
        self.assertEqual(tourney.tourney_type, "Store Championship")
        self.assertEqual(tourney.round_length, 60)
        self.assertEqual(tourney.participant_count, 30)
        self.assertEqual(tourney.venue.country, 'United States')
        self.assertEqual(tourney.venue.state, 'Illinois')
        self.assertEqual(tourney.venue.city, 'Chicago')
        self.assertEqual(tourney.venue.venue, 'Dice Dojo')

        #and the players/rankings
        self.assertEqual(len(tourney.tourney_players), 6)
        self.assertEqual(len(tourney.rankings), 6)
        p1 = tourney.tourney_players[0]
        p2 = tourney.tourney_players[2]
        self.assertEqual('Lyle Hayhurst', p1.player_name)
        self.assertEqual('Brandon Prokos', p2.player_name)

        self.assertEqual( 622, p1.result.mov)
        self.assertEqual( 50, p1.result.sos)
        self.assertEqual( 20, p1.result.score)
        self.assertEqual( False, p1.result.dropped)
        self.assertEqual( 1, p1.result.rank)
        self.assertEqual( 2, p1.result.elim_rank)

        self.assertEqual( 647, p2.result.mov)
        self.assertEqual( 45, p2.result.sos)
        self.assertEqual( 15, p2.result.score)
        self.assertEqual( True, p2.result.dropped)
        self.assertEqual( 2, p2.result.rank)
        self.assertEqual( 4, p2.result.elim_rank)


        #and finally the round by round results
        rounds = tourney.rounds
        self.assertEqual( 2, len(rounds ))
        pre_elim_rounds = tourney.get_pre_elimination_rounds()
        self.assertEqual( 1, len(pre_elim_rounds))
        r = pre_elim_rounds[0]
        self.assertEqual( 1, r.round_num)
        self.assertEqual( 'swiss', r.round_type_str())
        self.assertEqual( 2, len(r.results))
        res1 = r.results[0]
        res2 = r.results[1]
        self.assertEqual( "Lyle Hayhurst", res1.player1_name())
        self.assertEqual( "Brandon Prokos", res1.player2_name())
        self.assertEqual( p1, res1.winner.player)
        self.assertEqual( p2, res1.loser.player)
        self.assertEqual( "win", res1.get_result_for_json())
        self.assertEqual( 100, res1.list1_score)
        self.assertEqual( 48, res1.list2_score)

        id = tourney.id

        #ok, now try changing the tourney via various updates
        #first try changing the name
        t = {"tournament": {"name": "barbaz", 'date': "2000-01-01",
                            "type": "World Championship", "round_length": 61, "participant_count": 31,
                            'players': [
                                {
                                    "name": "Lyle Hayhurst",
                                    "new_name": "Kyle Hayhurst",
                                    "mov": 100,
                                    "score": 100,
                                    "sos": 100,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 5,
                                        "elimination": 10
                                    }
                                },
                                {
                                    "name": "New Player Bob",
                                    "mov": 100,
                                    "score": 100,
                                    "sos": 100,
                                    'dropped': True,
                                    "rank": {
                                        "swiss": 5,
                                        "elimination": 10
                                    }
                                },
                            ]
                    }
        }

        update_url = 'http://localhost:5000/api/v1/tournament/' + str(id)
        resp = put( update_url, data=json.dumps(t))
        self.assertEqual( 200, resp.status_code)
        js = resp.json()
        js = js['tournament']
        self.assertTrue(js.has_key('name'))
        self.assertTrue(js.has_key('id'))
        self.assertTrue(js['name'] == 'barbaz')

        #look it up
        pm.db_connector = myapp.MyDatabaseConnector()
        tourney2 = pm.get_tourney_by_id(int(js['id']))
        self.assertTrue(tourney2 is not None)
        self.assertEqual( "barbaz", tourney2.tourney_name)
        self.assertEqual( "2000-01-01", str(tourney2.tourney_date))
        self.assertEqual( "World Championship", tourney2.tourney_type)
        self.assertEqual( int(61), tourney2.round_length)
        self.assertEqual( int(31), tourney2.participant_count )

        #verify that the name change stuck
        player = tourney2.get_player_by_name("Lyle Hayhurst")
        self.assertTrue( player is None )
        player = tourney2.get_player_by_name("Kyle Hayhurst")
        self.assertTrue( player is not None)

        #and the rankings
        result = player.result
        self.assertTrue( result is not None )
        self.assertEqual( 100, result.mov )
        self.assertEqual( 100, result.sos )
        self.assertEqual( 100, result.score )
        self.assertEqual( 5, result.rank )
        self.assertEqual( 10, result.elim_rank )
        self.assertEqual( True, result.dropped )

        #and the new player
        player = tourney2.get_player_by_name("New Player Bob")
        self.assertTrue( player is not None)

        #and the rankings
        result = player.result
        self.assertTrue( result is not None )
        self.assertEqual( 100, result.mov )
        self.assertEqual( 100, result.sos )
        self.assertEqual( 100, result.score )
        self.assertEqual( 5, result.rank )
        self.assertEqual( 10, result.elim_rank )
        self.assertEqual( True, result.dropped )






        #ok, now delete the thing
        j = { "api_token": tourney.api_token }

        delete_url = 'http://localhost:5000/api/v1/tournament/' + str(id)
        resp = delete(delete_url ,
                    data=json.dumps(j))
        print resp.text
        self.assertEqual(204, resp.status_code)



    # tests various error conditions
    def testPutTournamentBad(self):
        #no data payload
        resp = post(dev_url,
                    data=None)
        self.assertEqual(403, resp.status_code)

        #empty data payload
        resp = post(dev_url,
                    data=json.dumps({}))
        self.assertEqual(403, resp.status_code)

        #no tournament fields
        resp = post(dev_url,
                    data=json.dumps({"tournament": {}}))
        self.assertEqual(403, resp.status_code)

        #missing required fields 1
        t = {"tournament": {"name": "foobar"}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(403, resp.status_code)

        #missing required fields 2
        t = {"tournament": {"name": "foobar", "date": "2015-05-25"}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(403, resp.status_code)

        #missing required fields 3
        t = {"tournament": {"name": "foobar", "date": "2015-05-25", "type": "Store Championship"}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(403, resp.status_code)

        #missing required fields 4
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(403, resp.status_code)

        #invalidly formatted date
        t = {"tournament": {"name": "foobar", "date": "foobar",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(403, resp.status_code)

        #invalidly formatted type
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Smore Championship", "round_length": 60, "participant_count": 30}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(403, resp.status_code)


if __name__ == "__main__":
    unittest.main()
