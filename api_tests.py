import json
import unittest
from requests import put, get, post, delete
import myapp
from persistence import PersistenceManager


dev_endpoint = 'http://localhost:5002/api/v1/'
dev_url  =  dev_endpoint + 'tournaments'
prod_url = 'http://lists.starwarsclubhouse.com/api/v1/tournaments'

class apiTest(unittest.TestCase):
    def testGetTournaments(self):
        resp = get(dev_url)
        ids = resp.json()
        self.assertTrue(ids is not None)
        self.assertTrue(len(ids) > 0)

    def testPutAndDeleteTournament(self):
        players = [{"name": "Lyle Hayhurst", "mov": 622, "score": 20, "sos": 2.00, 'dropped': False,
                         "rank": {"swiss": 1, "elimination": 2}},
                        {"name": "Matt Babiash", "mov": 647, "score": 15, "sos": 3.14, 'dropped': True,
                         "rank": {"swiss": 2, "elimination": 4}},
                        {"name": "Brandon Prokos", "mov": 647, "score": 15, "sos": 0.76, 'dropped': True,
                         "rank": {"swiss": 2, "elimination": 4}},
                        {"name": "Phil Kalata", "mov": 647, "score": 15, "sos": 45, 'dropped': True,
                         "rank": {"swiss": 2, "elimination": 4}},
                        {"name": "Zach Carriger", "mov": 647, "score": 15, "sos": 45, 'dropped': True,
                         "rank": {"swiss": 2, "elimination": 4}},
                        {"name": "David Pontier", "mov": 647, "score": 15, "sos": 45, 'dropped': True,
                         "rank": {"swiss": 2, "elimination": 4}}, ]

        trounds = [{"round-type": "swiss", "round-number": 1, "matches": [
            {"player1": "Lyle Hayhurst", "player1points": 100, "player2": "Brandon Prokos", "player2points": 48,
             "result": "win"},
            {"player1": "Zach Carriger", "player1points": 32, "player2": "Phil Kalata", "player2points": 0,
             "result": "win"}]}, {"round-type": "elimination", "round-number": 4, "matches": [
            {"player1": "Lyle Hayhurst", "player1points": 100, "player2": "Matt Babiash", "player2points": 80,
             "result": "win"},
            {"player1": "Phil Kalata", "player1points": 0, "player2": "David Pontier", "player2points": 100,
             "result": "win"}]}]

        sets = ["Core Set", "Wave 1", "Wave 2", "Wave 3", "Wave 4", "Wave 5", "Wave 6", "GR-75 Expansion",
                      "CR90 Expansion", "Imperial Aces Expansion", "Rebel Aces Expansion"]
        venue = {'country': 'United States', 'state': 'Illinois', 'city': 'Chicago', 'venue': 'Dice Dojo'}
        t = {"tournament": {"name": "foobar", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30,
                            'venue': venue,
                            'sets_used': sets,
                            'format': 'Standard - 100 Point Dogfight',
                            'players': players,
                            "rounds": trounds

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
        myapp.db_connector.close()
        myapp.db_connector.connect()
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

        #and the players/rankings
        self.assertEqual(len(tourney.tourney_players), 6)
        self.assertEqual(len(tourney.rankings), 6)
        p1 = tourney.tourney_players[0]
        p2 = tourney.tourney_players[2]
        self.assertEqual('Lyle Hayhurst', p1.player_name)
        self.assertEqual('Brandon Prokos', p2.player_name)

        self.assertEqual( 622, p1.result.mov)
        self.assertEqual( .99, p1.result.sos)
        self.assertEqual( 20, p1.result.score)
        self.assertEqual( False, p1.result.dropped)
        self.assertEqual( 1, p1.result.rank)
        self.assertEqual( 2, p1.result.elim_rank)

        self.assertEqual( 647, p2.result.mov)
        self.assertEqual( .76, p2.result.sos)
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

        #resubmit it to try to create dupes
        t['api_token'] = js['api_token']
        url = dev_endpoint + 'tournament/' + str(tourney.id)
        resp = put(url,
                    data=json.dumps(t))
        self.assertEqual(200, resp.status_code)

        #ok, change one of the results
        trounds[0]['matches'][0]['player1points'] =  99
        t['tournament']['name'] = 'changed name'
        resp = put(url,
                    data=json.dumps(t))
        self.assertEqual(200, resp.status_code)


        #ok, now delete the thing
        j = { "api_token": tourney.api_token }

        delete_url = dev_endpoint + 'tournament/' + str(id)
        resp = delete(delete_url ,
                    data=json.dumps(j))
        print resp.text
        self.assertEqual(204, resp.status_code)

    def isint(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def testAxelCase(self):
        t = {"tournament": {"name": "playertests", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30 } }
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(201, resp.status_code)
        tjson = resp.json()
        self.assertTrue( tjson is not None )
        tjson = tjson['tournament']
        tourney_id = tjson["id"]
        api_token = tjson['api_token']
        self.assertTrue( api_token is not None and len(api_token) > 0 )

        #add the players
        p =  [ { "name": "bob"}, {"name" : "bill"}  ]
        t = { 'api_token': api_token,
              'players': p
        }

        player_get_url = dev_endpoint + 'tournament/' + str(tourney_id) + "/players"
        resp = post( player_get_url , data=json.dumps(t))
        print resp.text
        self.assertEqual( 201, resp.status_code)
        pjson = resp.json()

        self.assertTrue(pjson.has_key('players'))
        players = pjson['players']
        bob = players[0]
        self.assertTrue( bob[ 'name'] == 'bob')
        self.assertTrue( bob.has_key( "id"))
        self.assertTrue (self.isint( bob['id']))
        self.assertTrue( int(bob['id'] > 0 ))

        bill = players[1]
        self.assertTrue( bill[ 'name'] == 'bill')
        self.assertTrue( bill.has_key( "id"))
        self.assertTrue (self.isint( bill['id']))
        self.assertTrue( int(bill['id'] > 0 ))

        p =  [
                      {
                          "player_id": bob['id'],
                          "mov": 622,
                          "score": 20,
                          "sos": 1.00,
                          'dropped': False,
                          "rank": {
                              "swiss": 1,
                              "elimination": 2
                          }
                      },
                      {
                          'player_id': bill['id'],
                          "mov": 647,
                          "score": 15,
                          "sos": 0.00,
                          'dropped': True,
                          "rank": {
                              "swiss": 2,
                              "elimination": 4
                          }
                      } ]

        #ok, now enter the rest of the data
        t = { 'api_token': api_token,
              'tournament': {
                  'format': 'Standard - 100 Point Dogfight',
                  'players': p ,
                  "rounds": [
                      {
                          "round-type": "swiss",
                          "round-number": 1,
                          "matches": [
                              {
                                  "player1_id": bob['id'],
                                  "player1points": 100,
                                  "player2_id":  bill['id'],
                                  "player2points": 48,
                                  "result": "win"
                              },
                          ]
                      }
                  ]
              }
        }
        url = dev_endpoint + 'tournament/' + str(tourney_id)

        resp = put(url,
                    data=json.dumps(t))
        self.assertEqual(200, resp.status_code)
        tjson = resp.json()
        self.assertTrue( tjson is not None )

        myapp.db_connector.close()
        myapp.db_connector.connect()
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        self.assertTrue( tourney is not None)
        self.assertTrue(len(tourney.tourney_players) == 2 )









    def testPlayerAPI(self):

        t = {"tournament": {"name": "playertests", "date": "2015-05-25",
                            "type": "Store Championship", "round_length": 60, "participant_count": 30,
                            "players": [ { "name": "bob"}, {"name" : "bill"}  ]}}
        resp = post(dev_url,
                    data=json.dumps(t))
        self.assertEqual(201, resp.status_code)
        tjson = resp.json()
        self.assertTrue( tjson is not None )
        tjson = tjson['tournament']
        tourney_id = tjson["id"]
        api_token = tjson['api_token']
        self.assertTrue( api_token is not None and len(api_token) > 0 )

        self.assertTrue( tourney_id is not None)
        players = tjson['players']
        self.assertTrue( len(players) == 2)
        bob = players[0]
        self.assertTrue( bob[ 'name'] == 'bob')
        self.assertTrue( bob.has_key( "id"))
        self.assertTrue (self.isint( bob['id']))
        self.assertTrue( int(bob['id'] > 0 ))

        bill = players[1]
        self.assertTrue( bill[ 'name'] == 'bill')
        self.assertTrue( bill.has_key( "id"))
        self.assertTrue (self.isint( bill['id']))
        self.assertTrue( int(bill['id'] > 0 ))

        #ok, get works just fine.
        #ty out player get
        player_get_url = dev_endpoint + 'tournament/' + str(tourney_id) + "/players"
        print player_get_url
        resp = get( player_get_url )
        print resp.text
        self.assertEqual( 200, resp.status_code)
        pjson = resp.json()

        self.assertTrue(pjson.has_key('players'))
        players = pjson['players']
        bob = players[0]
        self.assertTrue( bob[ 'name'] == 'bob')
        self.assertTrue( bob.has_key( "id"))
        self.assertTrue (self.isint( bob['id']))
        self.assertTrue( int(bob['id'] > 0 ))

        bill = players[1]
        self.assertTrue( bill[ 'name'] == 'bill')
        self.assertTrue( bill.has_key( "id"))
        self.assertTrue (self.isint( bill['id']))
        self.assertTrue( int(bill['id'] > 0 ))

        #and now the player put
        p = {"api_token": api_token,
            "players": [ { 'player_id': bob['id'], 'name': 'bob2' }, { 'player_id': bill['id'], 'name': 'bill2' }  ] }

        resp = put( player_get_url , data=json.dumps(p))
        print resp.text
        self.assertEqual( 200, resp.status_code)

        #look it up in the database and verify that the names were changed properly
        myapp.db_connector.close()
        myapp.db_connector.connect()
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        self.assertTrue( tourney is not None)

        p1 = tourney.get_player_by_name("bob2")
        self.assertTrue( p1 is not None )
        self.assertTrue( p1.player_name == "bob2")
        self.assertTrue( p1.id == bob['id'] )

        p2 = tourney.get_player_by_name("bill2")
        self.assertTrue( p2 is not None )
        self.assertTrue( p2.player_name == "bill2")
        self.assertTrue( p2.id == bill['id'] )

        #add some new names via post
        p = {"api_token": api_token,
            "players": [ {  'name': "joe"}, {  "name" : "jenny"}  ] }

        resp = post( player_get_url , data=json.dumps(p))
        print resp.text
        self.assertEqual( 201, resp.status_code)
        tjson = resp.json()
        self.assertTrue( tjson is not None )
        tjson = tjson['players']
        print tjson
        p1 = tjson[0]
        self.assertTrue( p1 is not None )
        self.assertTrue( p1['name'] == 'joe')
        self.assertTrue( p1['id'] is not None)
        p2 = tjson[1]
        self.assertTrue( p2 is not None )
        self.assertTrue( p2['name'] == 'jenny')
        self.assertTrue( p2['id'] is not None)

        #look it up in the database and verify that it stuck
        myapp.db_connector.close()
        myapp.db_connector.connect()
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        self.assertTrue( tourney is not None)

        dp1 = tourney.get_player_by_name("joe")
        self.assertTrue( dp1 is not None )
        self.assertTrue( dp1.player_name == "joe")
        self.assertTrue( dp1.id == p1['id'] )

        dp2 = tourney.get_player_by_name("jenny")
        self.assertTrue( dp2 is not None )
        self.assertTrue( dp2.player_name == "jenny")
        self.assertTrue( dp2.id == p2['id'] )

        #ok, now try to delete!
        #try to take out jenny

        d = {"api_token": api_token}
        delete_url = dev_endpoint + 'tournament/' + str(tourney_id) + "/player/" + str(p2['id'])
        resp = delete( delete_url , data=json.dumps(d))
        print resp.text
        self.assertEqual( 200, resp.status_code)

        myapp.db_connector.close()
        myapp.db_connector.connect()
        pm = PersistenceManager(myapp.db_connector)
        tourney = pm.get_tourney_by_id(tourney_id)
        self.assertTrue( tourney is not None)

        dp1 = tourney.get_player_by_name("joe")
        self.assertTrue( dp1 is not None )
        self.assertTrue( dp1.player_name == "joe")
        self.assertTrue( dp1.id == p1['id'] )

        dp2 = tourney.get_player_by_name("jenny")
        self.assertTrue( dp2 is  None )




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
