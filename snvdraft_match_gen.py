import copy
import random

if __name__ == '__main__':

    teams = {
        'Scum and Villainy': ['Kelvan', 'Sable Gryphon', 'Antigrapist', 'Blairbunke', 'Theorist', 'Sozin'],
        'Mynock Squadron': ['Dee Yun', 'Ryan Farmer', 'Dallas Parker', 'Joe Desmond', 'Minh Nguyen', 'Nick Belle'],
        'Rook/Nova': ['Paul Heaver', 'Majorjuggler', 'Phildo', 'Serrate', 'Jeff Berling', 'Jeff Faulkner'],
        'Team Aces': ['Mu0n', 'Starslinger', 'Dom', 'Remi', 'Darthdane', 'AssortedNeedles'],
        'Team Champions': ['Rinehart', 'Frans Bongers', 'Blade_Mercurial', 'BMF', 'JChavDanath', 'Tormentin'],
        'Team Commonwealth': ['Morgan Reid', 'Travis Foss', 'Jaren Foss', 'Mr. Sunol', 'The Dave Side', 'Dodo']
    }


    for t in teams.keys():
        i = 1
        for p in teams[t]:
            print "%s\t%s\tPlayer%d" % ( t, p, i )
            i += 1

    player_to_team = {}
    player_match_count = {}
    player_matches = {}
    for team in teams.keys():
        players = teams[team]
        for player in players:
            player_to_team[player] = team
            player_match_count[player] = 0
            player_matches[player] = []

    shuffled_team_names = teams.keys()
    random.shuffle(shuffled_team_names)

    for team in shuffled_team_names:
        for player in teams[team]:
            num_matches_to_schedule = 3-player_match_count[player]
            if num_matches_to_schedule >0: #matches still to schedule

                potential_player_opponent_teams = teams.keys()
                potential_player_opponent_teams.remove( team )
                my_matches = player_matches[player]
                opponents = {}
                teams_played = {}

                for m in my_matches:
                    opponents_team = player_to_team[m[1]]
                    if not teams_played.has_key(opponents_team):
                        teams_played[opponents_team] = True
                        potential_player_opponent_teams.remove(opponents_team)

                for pt in potential_player_opponent_teams:
                    for po in teams[pt]:
                        opponents_team = player_to_team[po]
                        #only add the player if 1) we haven't played their team yet and 2) they still have games left to play and 3) they haven't played anyone on our team
                        havent_played_our_team = True
                        opponents_matches = player_matches[po]
                        for om in opponents_matches:
                            if team == player_to_team[om[1]]:
                                havent_played_our_team = False
                        if player_match_count[po] < 3 and havent_played_our_team:
                            if not opponents.has_key(pt):
                                opponents[pt] = []
                            opponents[pt].append(po)

                if len(opponents.keys()) == 0:
                    print "unable to schedule player %s" % ( player )
                    break

                actual_opponent_teams = opponents.keys()
                random.shuffle(actual_opponent_teams)

                matches_to_schedule = 3-player_match_count[player]
                i = 0
                while matches_to_schedule > 0:
                    if i >= len(actual_opponent_teams):
                        print "unable to schedule player %s" % ( player)
                        matches_to_schedule = 0
                    else:
                        ppot = actual_opponent_teams[i]
                        potential_opponents = opponents[ppot]
                        opponent = random.choice(potential_opponents)
                        player_matches[player].append([player,opponent])
                        player_matches[opponent].append([opponent,player])
                        player_match_count[player] += 1
                        player_match_count[opponent] += 1
                        matches_to_schedule -= 1
                        i = i +1

    print "PLAYER1\tPLAYER1_TEAM\tPLAYER2\tPLAYER2_TEAM"
    for player in player_matches.keys():
        for m in player_matches[player]:
            player1 = m[0]
            player2 = m[1]
            team1   = player_to_team[player1]
            team2   = player_to_team[player2]
            print "%s\t%s\t%s\t%s" % ( player1, team1, player2, team2 )

