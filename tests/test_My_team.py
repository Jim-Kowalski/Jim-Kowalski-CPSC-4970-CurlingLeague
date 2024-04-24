import unittest
from model.team import Team, DuplicateEmail
from model.team_member import TeamMember
from tests.fake_emailer import FakeEmailer
from model.custom_exceptions import DuplicateOid
class TeamTests(unittest.TestCase):
    def test_create(self):
        name = "Curl Jam"
        oid = 10
        t = Team(oid, name)
        self.assertEqual(name, t.name)
        self.assertEqual(oid, t.oid)

    def test_adding_adds_to_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        tm3 = TeamMember(7, "h", "duplicateEmail@duplicate.com")
        tm4 = TeamMember(8, "i", "DupLICaTeEmAIL@DUPLICATE.cOm")
        #test that a member was addedd
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        self.assertNotIn(tm2, t.members)

        t.add_member(tm2)
        self.assertIn(tm1, t.members)
        self.assertIn(tm2, t.members)

        #test that adding a duplicate member to the team throws a DuplicateOid exception
        with self.assertRaises(DuplicateOid):
            t.add_member(tm1)

        #test that adding a member with a duplicate email causes a DuplicateEmail exception
        with self.assertRaises(DuplicateEmail):
            t.add_member(tm3)
            t.add_member(tm4) #This member is not added

        self.assertIn(tm3, t.members)

        self.assertEqual(3, len(t.members))


    def test_removing_removes_from_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        t.add_member(tm2)
        t.remove_member(tm1)
        self.assertNotIn(tm1, t.members)
        self.assertIn(tm2, t.members)

    def test_member_named(self):
        t = Team(1, "Flintstones")
        t.add_member(TeamMember(2, "Fred", "fred@bedrock"))
        t.add_member(TeamMember(3, "Barney", "barney@bedrock"))
        t.add_member(TeamMember(4, "Wilma", "wilma@bedrock"))
        self.assertEqual(t.members[0], t.member_named("Fred"))
        self.assertEqual(t.members[1], t.member_named("Barney"))
        self.assertEqual(t.members[2], t.member_named("Wilma"))
        self.assertIsNone(t.member_named("fred"))

    def test_sends_email(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f@foo.com")
        tm2 = TeamMember(6, "g", "g@bar.com")
        tm3 = TeamMember(7, "h", None)
        t.add_member(tm1)
        t.add_member(tm2)
        t.add_member(tm3)
        fe = FakeEmailer()
        t.send_email(fe, "Subject", "Message")
        self.assertIn("f@foo.com", fe.recipients)
        self.assertIn("g@bar.com", fe.recipients)
        self.assertEqual(2, len(fe.recipients))
        self.assertEqual("Subject", fe.subject)
        self.assertEqual("Message", fe.message)


    def test_str_method(self):
        t = Team(1, "Flintstones")
        t.add_member(TeamMember(2, "Fred", "fred@bedrock"))
        t.add_member(TeamMember(3, "Barney", "barney@bedrock"))
        t.add_member(TeamMember(4, "Wilma", "wilma@bedrock"))
        # Test __str__ method
        expected_output = "Team Flintstones: 3 members"
        self.assertEqual(str(t), expected_output)


if __name__ == '__main__':
    unittest.main()
