import unittest
from model.competition import Competition
from model.team import Team
from model.team_member import TeamMember
from datetime import datetime
from tests.fake_emailer import FakeEmailer


class TestCompetition(unittest.TestCase):
    def test_initialization(self):
        oid = 1
        teams = ["Team A", "Team B"]
        location = "Stadium"
        date_time = datetime(2024, 3, 30, 18, 0, 0)
        competition = Competition(oid, teams, location, date_time)
        self.assertEqual(oid, competition.oid)
        self.assertEqual(teams, competition.teams_competing)
        self.assertEqual(location, competition.location)
        self.assertEqual(date_time, competition.date_time)

    def test_str_with_date_time(self):
        oid = 1
        teams = ["Team A", "Team B"]
        location = "Stadium"
        date_time = datetime(2024, 3, 30, 18, 0, 0)
        competition = Competition(oid, teams, location, date_time)
        self.assertEqual(str(competition), f"Competition at {location} on 03/30/2024 18:00 with 2 teams")

    def test_str_without_date_time(self):
        oid = 1
        teams = ["Team A", "Team B"]
        location = "Stadium"
        competition = Competition(oid, teams, location, None)
        self.assertEqual(str(competition), f"Competition at {location} with 2 teams")

    def test_date_time_setter(self):
        oid = 1
        teams = ["Team A", "Team B"]
        location = "Stadium"
        date_time = datetime(2024, 3, 30, 18, 0, 0)
        competition = Competition(oid, teams, location, None)
        competition.date_time = date_time
        self.assertEqual(date_time, competition.date_time)

    def test_location_setter(self):
        oid = 1
        teams = ["Team A", "Team B"]
        location = "Stadium"
        new_location = "Arena"
        competition = Competition(oid, teams, location, None)
        competition.location = new_location
        self.assertEqual(new_location, competition.location)

    def test_send_email(self):

        t1 = Team(1, "Flintstones")
        tm1 = TeamMember(2, "fred", "fredflinstone@bedrock.com")
        tm2 = TeamMember(3, "barney", "barneyrubble@bedrock.com")
        tm3 = TeamMember(4, "wilma", "wilmaflinstones@bedrock.com")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t1.add_member(tm3)

        t2 = Team(12, "Jetsons")
        tm21 = TeamMember(13, "george", "fredflinstone@earth.com")
        tm22 = TeamMember(14, "rosie", "barneyrubble@earth.com")
        tm23 = TeamMember(15, "Jane", None)
        t2.add_member(tm21)
        t2.add_member(tm22)
        t2.add_member(tm23)

        t3 = Team(12, "Jetsons")
        tm31 = TeamMember(16, "george", "georgeflinstone@earth.com")
        tm32 = TeamMember(17, "rosie", "barneyrubble@earth.com")
        tm33 = TeamMember(18, "Jane", "Jane@earth.com")
        t3.add_member(tm31)
        t3.add_member(tm32)
        t3.add_member(tm33)

        teams = [t1, t2, t3]
        location = "Stadium"
        date_time = datetime(2024, 3, 30, 18, 0, 0)
        competition = Competition(222, teams, location, date_time)
        fe = FakeEmailer()
        competition.send_email(fe, "Test", "This is a test")

if __name__ == '__main__':
    unittest.main()
