from model.identified_object import IdentifiedObject
from model.custom_exceptions import DuplicateEmail,DuplicateOid
class Team(IdentifiedObject):
    def __init__(self, oid, name):
        """
        Initializes a Team object with the specified OID and name.

        :param oid: The unique identifier of the team.
        :param name: The name of the team.
        """
        super().__init__(oid)
        self._members = []
        self.name = name

    """
    A class representing a team.
    """
    @property
    def name(self):
        """
        Property representing the team name.

        :return: The name of the team.
        """
        #[prop]
        return self._name
    @name.setter
    def name(self, new_name):
        """
         Setter for the team name property.

         :param new_name: The new name for the team.
         """
        #[prop]
        self._name = new_name

    @property
    def members(self):
        """
        Read-only property representing the list of team members.

        :return: List of team members.
        """
        #[r/o prop] -- list of team members
        # return all members to the caller
        return self._members[:]



    def __str__(self):
        """
        Returns a string representation of the team.

        :return: A string representation of the team.
        """
        #  return a string like the following: "Team Name: N members"
        return f"Team {self.name}: {len(self.members)} members"

    def add_member(self, member):
        """
        Adds a member to the team unless they are already a member.

        :param member: The member to add.
        :raises DuplicateEmail: If the member's email already exists in the team.
        :raises DuplicateOid: If the member's OID already exists in the team.
        """
        #ignore request to add team member that is already in members
        if member is None:
            return
        if member not in self.members:
            email_values = [_member.email.lower() for _member in self._members[:]]
            if member.email == None or not member.email.lower() in email_values:
                self._members.append(member)
            else:
                raise DuplicateEmail(member.email)
        else:
            raise DuplicateOid(member.oid)

    def find_free_member_oid(self):
        # gather the used oid's in the collection of members.
        used_oids = {member.oid for member in self._members}

        # Start with oid 1 and count up to the length of the number of teams
        # in the list. If there are 4 teams, and there are oid gaps, at least
        # one oid will be missing. So, the algorithm will return the missing oid.

        # If there are no gaps, we allow an additional couple of indexes
        # and will select the oid that exceeds the last known oid.
        for oid in range(1, len(self._members) + 2):
            if oid not in used_oids:
                return oid
        return None  # If no free oid is found

    def member_named(self, s):
        """
        Retrieves the member of this team whose name equals s (case-sensitive).

        :param s: The name of the member to retrieve.
        :return: The member with the specified name or None if not found.
        """
        #return the member of this team whose name equals s (case sensitive) or None if no such member exists
        for member in self.members:
            if member.name == s:
                return member
                break


    def remove_member(self, member):
        """
        Removes the specified member from this team.

        :param member: The member to remove.
        """
        #remove the specified member from this team
        if member in self._members:
            self._members.remove(member)

    def send_email(self, emailer, subject, message):
        """
        Sends an email to all members of the team.

        :param emailer: The emailer object used to send the email.
        :param subject: The subject of the email.
        :param message: The message content of the email.
        """
        # use the emailer argument to send an email to all members of a team except those whose email address is None.
        # This method should send a single email so if the team has N members, the recipient list will have N elements.
        recipient_list = []
        for member in self.members:
            if member.email is not None:
                recipient_list.append(member.email)

        emailer.send_plain_email(recipient_list, subject, message)
