from model.identified_object import IdentifiedObject

class Competition(IdentifiedObject):
    """
    A class representing a competition.
    """
    def __init__(self, oid, teams, location, datetime):
        """
        Initializes a Competition object with the specified OID, teams, location, and datetime.

        :param oid: The unique identifier of the competition.
        :param teams: A list containing two teams that are competing against each other.
        :param location: The location of the competition.
        :param datetime: Optional. A Python datetime object indicating when the competition will begin.
        """
        # initialization method that sets the oid, teams, location and date_time properties as specified
        # in the arguments (note: should call superclass constructor).  Note: teams should be a list.
        # See above for the type of the datetime argument.
        super().__init__(oid)
        self._teams = teams
        self._location = location
        self._datetime = datetime

    def __str__(self):
        """
        Returns a string representation of the competition.

        :return: A string representation of the competition.
        """
        # return a string like the following: "Competition at location on date_time with N teams"
        # (note: date_time may be None in which case just omit the "on date_time" part.  If present,
        # format the date_time property similar to the following example "12/31/1995 19:30".
        formatted_date = "" if self.date_time is None  else( f'on {self.date_time.strftime("%m/%d/%Y %H:%M")} ')
        return f"Competition at {self.location} {formatted_date}with {len(self.teams_competing)} teams"


    @property
    def teams_competing(self):
        """
        Read-only property representing the list containing two teams that are competing against each other.

        :return: List containing two teams that are competing against each other.
        """
        #[r/o prop] -- list containing two teams that are competing against each other
        return self._teams

    @property
    def date_time(self):
        """
        Property representing the date and time when the competition will begin.

        :return: A Python datetime object indicating when the competition will begin.
        """
        #[prop] -- optional (may be None) -- a Python datetime objects (not a string!) indicating when the competition will begin.
        return self._datetime

    @date_time.setter
    def date_time(self, new_date_time):
        """
        Setter for the date and time of the competition.

        :param new_date_time: The new date and time for the competition.
        """
        self._datetime = new_date_time

    @property
    def location(self):
        """
        Property representing the location of the competition.

        :return: The location of the competition.
        """
        return self._location

    @location.setter
    def location(self, new_location):
        """
        Setter for the location of the competition.

        :param new_location: The new location for the competition.
        """
        self._location = new_location

    def send_email(self, emailer, subject, message):
        """
        Sends an email to all members of all teams in this competition without duplicates.

        :param emailer: The emailer object used to send the email.
        :param subject: The subject of the email.
        :param message: The message content of the email.
        """
        # use the emailer argument to send an email to all members of all teams in this competition without
        # duplicates.  That is, a team member may be on multiple teams that may be competing against each
        # other.  Only send one email to each team member on all of the teams in this competition.  This
        # method should send a single email so if the teams have N and M members respectively, the recipient
        # list will have N+M elements assuming all of the members were distinct.  If the teams have S "shared"
        # members then we'd expect a single email with N+M-S recipients.
        recipient_list = []
        members = []
        for team in self.teams_competing:
            for member in team.members:
                if member not in members:
                    members.append(member)
                    if member.email is not None and member.email != "":
                        if member.email not in recipient_list:
                            recipient_list.append(member.email)

        if recipient_list is not None:
            emailer.send_plain_email(recipient_list, subject, message)


        
        

