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
