import os
import unittest
import challonge


class ChallongeHelper:
    def __init__(self, user, api_key):
        challonge.set_credentials(user, api_key)

    def get_tournament(self, tid):
        return challonge.tournaments.show(tid)

    def get_index(self):
        return challonge.tournaments.index()

    def create_tournament(self, name, url, tournament_type, params):
        challonge.tournaments.create(name, url, tournament_type, **params)

    def create_participant(self,tournament, name, params ):
        challonge.participants.create( tournament, name, **params)

    def update_participant(self, tournament, participant_id, params):
        challonge.participants.update( tournament, participant_id, **params )

    def participant_index(self, tournament):
        return challonge.participants.index(tournament)

    def match_index(self, tournament):
        return challonge.matches.index(tournament)

    def attachments_index(self, tournament, match_id):
        url = "tournaments/%s/matches/%s/attachments" % (tournament, match_id)
        return challonge.api.fetch_and_parse("GET", url)

class challongeAPITest(unittest.TestCase):

    def __init__(self,*args, **kwargs):
        super(challongeAPITest, self).__init__(*args, **kwargs)
        challonge_user = os.getenv('CHALLONGE_USER')
        challonge_key  = os.getenv('CHALLONGE_API_KEY')
        self.ch = ChallongeHelper(challonge_user, challonge_key)

    def testGetTournament(self):
        i = self.ch.get_tournament("XWingVassalLeagueSeasonZero")
        print i

if __name__ == "__main__":
    unittest.main()