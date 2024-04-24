import csv
from model.identified_object import IdentifiedObject
from model.custom_exceptions import DuplicateOid
from model.team import Team
from model.team_member import TeamMember
class League(IdentifiedObject):
    """
    A class representing a sports league.
    """
    def __init__(self, oid, name):
        """
        Initializes a League object with the specified OID and name.

        :param oid: The unique identifier of the league.
        :param name: The name of the league.
        """
        super().__init__(oid)
        self._name = name
        self._teams = []
        self._competitions = []

    @property
    def name(self):
        """
        Property representing the league name.

        :return: The name of the league.
        """
        # [prop] -- the league name
        return self._name

    @name.setter
    def name(self, new_name):
        """
        Setter for the league name property.

        :param new_name: The new name for the league.
        """
        # [prop] -- the league name
        self._name = new_name

    @property
    def teams(self):
        """
        Read-only property representing the list of teams participating in this league.

        :return: List of teams participating in this league.
        """
        # [r/o prop] -- list of teams participating in this league
        return self._teams[:]

    @property
    def competitions(self):
        """
        Read-only property representing the list of competitions (games) associated with this league.

        :return: List of competitions associated with this league.
        """
        #[r/o prop] -- list of competitions (games)
        return self._competitions

    def add_team(self, team):
        """
        Adds a team to the teams collection unless it is already present.

        :param team: The team to add.
        :raises DuplicateOid: If the team's OID already exists.
        """
        #add team to the teams collection unless they are already in it (in which case do nothing)
        if team not in self.teams:
            self._teams.append(team)
        else:
            raise DuplicateOid(team.oid)

    def remove_team(self, team):
        """
        Removes a team from the teams collection if it's not participating in any competition.

        :param team: The team to remove.
        :raises ValueError: If the team is competing in a competition.
        """
        #Ensure that the team being removed is not competing or throw a value error.
        for competition in self.competitions:
            if team in competition.teams_competing:
                raise ValueError(f"{team.name} in competition and cannot be removed!")

        # remove the team if they are in the teams list, otherwise do nothing
        if team in self.teams:
            self._teams.remove(team)

    def find_free_team_oid(self):
        # gather the used oid's in the collection of leagues.
        used_oids = {team.oid for team in self._teams}

        # Start with oid 1 and count up to the length of the number of teams
        # in the list. If there are 4 teams, and there are oid gaps, at least
        # one oid will be missing. So, the algorithm will return the missing oid.

        # If there are no gaps, we allow an additional couple of indexes
        # and will select the oid that exceeds the last known oid.
        for oid in range(1, len(self._teams) + 2):
            if oid not in used_oids:
                return oid
        return None  # If no free oid is found


    def team_named(self, team_name):
        """
        Retrieves the team with the specified name from the league's teams.

        :param team_name: The name of the team to retrieve.
        :return: The team with the specified name or None if not found.
        """
        # return the team in this league whose name equals team_name (case sensitive) or None if no such team exists
        for team in self.teams:
            if team.name == team_name:
                return team
        return None

    def add_competition(self, competition):
        """
        Adds a competition to the competitions collection if all participating teams belong to the league.

        :param competition: The competition to add.
        :raises ValueError: If any participating team is not a member of the league.
        :raises DuplicateOid: If the competition's OID already exists.
        """
        for team in competition.teams_competing:
            if not self.team_named(team.name):
                raise ValueError(f"{team.name} not in league")

        # add competition to the competitions collection
        if  competition not in self.competitions:
            self._competitions.append(competition);
        else:
            raise DuplicateOid(competition.oid)

    def teams_for_member(self, member):
        """
        Retrieves a list of teams for which the member plays.

        :param member: The member to retrieve teams for.
        :return: A list of teams for which the member plays.
        """
        # return a list of all teams for which member plays
        teams = []
        for team in self.teams:
            if member in team.members:
                if team not in teams:
                    teams.append(team)

        return teams

    def competitions_for_team(self, team):
        """
        Retrieves a list of competitions in which the team is participating.

        :param team: The team to retrieve competitions for.
        """
        # return a list of all competitions in which team is participating
        return_competitions = []
        for competition in self.competitions:
            if team in competition.teams_competing:
                if competition not in return_competitions:
                    return_competitions.append(competition)
        return return_competitions


    def competitions_for_member(self, member):
        """
        Retrieves a list of competitions for which the member played on one of the competing teams.

        :param member: The member to retrieve competitions for.
        :type member: Member
        """
        # return a list of all competitions for which member played on one of the competing teams
        return_competitions = []
        for competition in self.competitions:
            for team in competition.teams_competing:
                if member in team.members:
                    if competition not in return_competitions:
                        return_competitions.append(competition)
        return return_competitions

    def export_league_team(self, team, file_name):
        """
        Writes the specified league to a CSV formatted file.

        :param league: The league to export.
        :param file_name: The name of the CSV file to export to.
        """
        # write the specified league to a CSV formatted file.  The first line of the file must be a "header" row containing the following text (without the leading spaces):
        # Team name, Member name, Member email
        # If an error occurs while writing a league, display a message on the console.
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Team name', 'Member name', 'Member email'])
                for member in team.members:
                    writer.writerow([team.name, member.name, member.email])
        except Exception as e:
            print(f"Error exporting league team: {e}")

    def import_league_team(self, file_name):
        """
        Loads the teams and team members in a league from a CSV formatted file.

        :param league: The league to load teams into.
        :param file_name: The name of the CSV file to import.
        """
        try:

            with open(file_name, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # skip header

                for row in reader:
                    # Read the row
                    team_name, member_name, member_email = row

                    # Determine if the team is in the league
                    team = self.team_named(team_name)

                    # If the team is not in the league, we will create it
                    if not team:
                        new_oid = self.find_free_team_oid()
                        team = Team(new_oid, team_name)
                        self.add_team(team)

                    team = self.team_named(team_name)
                    if team:
                        member = team.member_named(member_name)

                        # if there is not a member or the new member email is different than the
                        # member email in the team, we'll create a new member and add it to the
                        # team.
                        if not member or member.email.tolower() != member_email.tolower():
                            new_oid = team.find_free_member_oid()
                            member = TeamMember(new_oid, member_name, member_email)
                            team.add_member(member)


        except Exception as e:
            print(f"Error import_league_teams: {e}")



    def __str__(self):
        """
        Returns a string representation of the league.
        """
        # return a string resembling the following: "League Name: N teams, M competitions" where N and M are replaced by the obvious values
        team_count = 0
        unique_teams = []
        for competition in self.competitions:
            for team in competition.teams_competing:
                if team.name not in unique_teams:
                    unique_teams.append(team.name)
        team_count += len(unique_teams)
        return f"League {self.name}: {team_count} teams, {len(self.competitions)} competitions"