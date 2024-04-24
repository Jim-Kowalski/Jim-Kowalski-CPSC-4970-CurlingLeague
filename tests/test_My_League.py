import unittest
from model.competition import Competition
from model.league import League
from model.team import Team
from model.team_member import TeamMember
import datetime
class TestLeague(unittest.TestCase):
    def test_create(self):
        league = League(1, "AL State Curling League")
        self.assertEqual(1, league.oid)
        self.assertEqual("AL State Curling League", league.name)
        self.assertEqual([], league.teams)
        self.assertEqual([], league.competitions)

    def test_adding_team_adds_to_teams(self):
        t = Team(1, "Ice Maniacs")
        league = League(1, "AL State Curling League")
        self.assertNotIn(t, league.teams)
        league.add_team(t)
        self.assertIn(t, league.teams)

    def test_adding_competition_adds_to_competitions(self):
        c = Competition(1, [], "Local tourney", None)
        league = League(13, "AL State Curling League")
        self.assertNotIn(c, league.competitions)
        league.add_competition(c)
        self.assertIn(c, league.competitions)

    def test_adding_competition_to_League_with_foreign_team_causes_exception(self):
        t = Team(1, "Ice Maniacs")
        c = Competition(1, [t,t], "Local tourney", None)
        league = League(13, "AL State Curling League")
        self.assertNotIn(c, league.competitions)

        #adding a competition with teams not in the league throws an exception.
        with self.assertRaises(ValueError):
            league.add_competition(c)

    def test_removing_team_involve_in_competition_causes_exception(self):
        league = self.build_league()
        t1 = Team(1, "t1")
        with self.assertRaises(ValueError):
            league.remove_team(t1)

    @staticmethod
    def build_league():
        league = League(1, "Some league")
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

    def test_team_named(self):
        league = self.build_league()
        t = league.team_named("t1")
        self.assertEqual(league.teams[0], t)
        t = league.team_named("t3")
        self.assertEqual(league.teams[2], t)
        t = league.team_named("bogus")
        self.assertIsNone(t)

    def test_big_league(self):
        league = self.build_league()
        t = league.teams[0]
        cs = league.competitions_for_team(t)
        # matchups are (t1, t2), (t1, t3), (t2, t1), (t3, t1) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t1 vs t2", "t1 vs t3", "t2 vs t1", "t3 vs t1"}, cs_names)

        self.assertEqual([league.teams[2]], league.teams_for_member(league.teams[2].members[0]))

        # Grab a player from the third team
        cs = league.competitions_for_member(league.teams[2].members[0])
        # matchups are (t3, t1), (t3, t2), (t2, t3), (t1, t3) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t3 vs t1", "t3 vs t2", "t2 vs t3", "t1 vs t3"}, cs_names)

    def test_str_method(self):
        # Create some teams
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        team3 = Team(3, "Team 3")
        now = datetime.datetime.now()
        # Create some competitions
        competition1 = Competition(1, [team1, team2], "Here", None)
        competition2 =  Competition(2, [team2, team3], "There", now)

        # Create a league
        league = League(201, "Test League")

        # Add teams and competitions to the league
        league.add_team(team1)
        league.add_team(team2)
        league.add_team(team3)

        league.add_competition(competition1)
        league.add_competition(competition2)
        # Test __str__ method
        expected_output = "League Test League: 3 teams, 2 competitions"
        self.assertEqual(str(league), expected_output)

    def test_teams_for_member(self):
        league = League(1, "Test League")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        team3 = Team(3, "Team 3")

        member1 = TeamMember(1, "Alice", "alice@example.com")
        member2 = TeamMember(2, "Bob", "bob@example.com")
        member3 = TeamMember(3, "Charlie", "charlie@example.com")

        team1.add_member(member1)
        team2.add_member(member2)
        team3.add_member(member3)

        league.add_team(team1)
        league.add_team(team2)
        league.add_team(team3)

        member_teams = league.teams_for_member(member1)
        self.assertIn(team1, member_teams)
        self.assertNotIn(team2, member_teams)
        self.assertNotIn(team3, member_teams)

        member_teams = league.teams_for_member(member2)
        self.assertNotIn(team1, member_teams)
        self.assertIn(team2, member_teams)
        self.assertNotIn(team3, member_teams)

        member_teams = league.teams_for_member(member3)
        self.assertNotIn(team1, member_teams)
        self.assertNotIn(team2, member_teams)
        self.assertIn(team3, member_teams)

    def test_competitions_for_team(self):
        league = League(1, "Test League")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        team3 = Team(3, "Team 3")

        member1 = TeamMember(1, "Alice", "alice@example.com")
        member2 = TeamMember(2, "Bob", "bob@example.com")
        member3 = TeamMember(3, "Charlie", "charlie@example.com")

        team1.add_member(member1)
        team2.add_member(member2)
        team3.add_member(member3)

        league.add_team(team1)
        league.add_team(team2)
        league.add_team(team3)

        competition1 = Competition(1, [team1, team2], "Competition 1", None)
        competition2 = Competition(2, [team2, team3], "Competition 2", None)

        league.add_competition(competition1)
        league.add_competition(competition2)

        team1_competitions = league.competitions_for_team(team1)
        self.assertIn(competition1, team1_competitions)
        self.assertNotIn(competition2, team1_competitions)

        team2_competitions = league.competitions_for_team(team2)
        self.assertIn(competition1, team2_competitions)
        self.assertIn(competition2, team2_competitions)

        team3_competitions = league.competitions_for_team(team3)
        self.assertNotIn(competition1, team3_competitions)
        self.assertIn(competition2, team3_competitions)

    def test_competitions_for_member(self):
        league = League(1, "Test League")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        team3 = Team(3, "Team 3")

        member1 = TeamMember(1, "Alice", "alice@example.com")
        member2 = TeamMember(2, "Bob", "bob@example.com")
        member3 = TeamMember(3, "Charlie", "charlie@example.com")

        team1.add_member(member1)
        team2.add_member(member2)
        team3.add_member(member3)

        league.add_team(team1)
        league.add_team(team2)
        league.add_team(team3)

        competition1 = Competition(1, [team1, team2], "Competition 1", None)
        competition2 = Competition(2, [team2, team3], "Competition 2", None)

        league.add_competition(competition1)
        league.add_competition(competition2)

        member1_competitions = league.competitions_for_member(member1)
        self.assertIn(competition1, member1_competitions)
        self.assertNotIn(competition2, member1_competitions)

        member2_competitions = league.competitions_for_member(member2)
        self.assertIn(competition1, member2_competitions)
        self.assertIn(competition2, member2_competitions)

        member3_competitions = league.competitions_for_member(member3)
        self.assertNotIn(competition1, member3_competitions)
        self.assertIn(competition2, member3_competitions)


if __name__ == '__main__':
    unittest.main()
