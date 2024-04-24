import unittest
import random
import os
from model.league import League
from model.team import Team
from model.team_member import TeamMember
from model.league_database import LeagueDatabase
from model.competition import Competition


class TestLeagueDatabase(unittest.TestCase):

    @staticmethod
    def build_league(oid = 1):
        league = League(oid, "Some league")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        all_teams = [t1, t2, t3]
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Barney", "barney")
        tm3 = TeamMember(3, "Wilma", "wilma")
        tm4 = TeamMember(4, "Betty", "betty")
        tm5 = TeamMember(5, "Pebbles", "pebbles")
        tm6 = TeamMember(6, "Bamm-Bamm", "bam-bam")
        tm7 = TeamMember(7, "Dino", "dino")
        tm8 = TeamMember(8, "Mr. Slate", "mrslate")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm3)
        t2.add_member(tm4)
        t2.add_member(tm5)
        t3.add_member(tm6)
        t3.add_member(tm7)
        t3.add_member(tm8)
        # every team plays every other team twice
        oid = 1
        for c in [Competition(oid := oid + 1, [team1, team2], team1.name + " vs " + team2.name, None)
                  for team1 in all_teams
                  for team2 in all_teams
                  if team1 != team2]:
            league.add_competition(c)
        return league
    @staticmethod
    def build_leagues(num_leagues):
        # Lists of names to generate unique names for leagues, teams, and members
        league_names = ["USA Premier League", "UEFA", "Mexican LIGA", "Series A", "FIFA", "German Bundesliga"]
        team_prefixes = ["FC", "United", "City", "Real", "Barcelona", "Los Angeles", "Berlin", "Paris"]
        first_names = ["Fred", "Barney", "Wilma", "Betty", "Pebbles", "Bamm-Bamm", "Dino", "Mr. Slate"]
        last_names = ["Jones", "Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson"]

        leagues = []
        for league_id in range(1, num_leagues + 1):
            # Generate a unique name for the league
            league_name = f"{random.choice(league_names)} {league_id}"
            league = League(league_id, league_name)
            teams = []
            # Create teams for the league
            for team_id in range(1, 4):
                team_name = f"{random.choice(team_prefixes)} {team_id} {league_id}"
                team = Team(team_id, team_name)
                teams.append(team)
                league.add_team(team)
                for member_id in range(1, 4):
                    first_name = random.choice(first_names)
                    last_name = random.choice(last_names)
                    full_name = f"{first_name} {last_name}"
                    member_username = f"member_{league_id}_{team_id}_{member_id}"
                    team_member = TeamMember(member_id, full_name, member_username)
                    team.add_member(team_member)

            # Create competitions
            oid = 0
            for team1 in teams:
                for team2 in teams:
                    if team1 != team2:
                        oid += 1
                        competition = Competition(oid, [team1, team2], f"{team1.name} vs {team2.name}", None)
                        league.add_competition(competition)

            leagues.append(league)
        return leagues

    def setUp(self):
        self.db = LeagueDatabase.instance()

        #------------------------------------------------------------------------------
        # Clear out all the leagues if there are any
        #------------------------------------------------------------------------------
        if len(self.db.leagues) > 0:
            leagues_to_remove = []
            for league in self.db.leagues:
                leagues_to_remove.append(league.name)

            for league_name in leagues_to_remove:
                league = self.db.league_named(league_name)
                if not league is None:
                    self.db.remove_league(league)

        # leagues = TestLeagueDatabase.build_leagues(2)  # Clear any existing leagues
        # for league in leagues:
        #     self.db.add_league(league)

    def test_add_league(self):
        test_league = TestLeagueDatabase.build_league(3)
        self.db.add_league(test_league)
        self.assertIn(test_league, self.db.leagues)
        self.db = None



    def test_remove_league(self):

        test_league = TestLeagueDatabase.build_league(3)
        self.db.add_league(test_league)
        self.db.remove_league(test_league)
        self.assertNotIn(test_league, self.db.leagues)
        self.db = None


    def test_league_named(self):
        test_league = TestLeagueDatabase.build_league(3)
        self.db.add_league(test_league)
        league = self.db.league_named("Some league")
        self.assertEqual(league, test_league)
        self.db = None



    def test_load_database_when_file_does_not_exist(self):
        if os.path.exists("d:\\test_db.pkl"):
            os.remove("d:\\test_db.pkl")
        new_db = LeagueDatabase.instance()
        new_db.load("test_db.pkl")

    def test_import_export_teams(self):
        test_league = TestLeagueDatabase.build_league(3)
        self.db.add_league(test_league)
        my_league = self.db.league_named("Some league")
        self.db.import_league_teams(my_league, "d:\\teams.csv")
        self.db.export_league_teams(my_league, "d:\\exported_teams.csv")
        self.db = None

if __name__ == '__main__':
    unittest.main()
