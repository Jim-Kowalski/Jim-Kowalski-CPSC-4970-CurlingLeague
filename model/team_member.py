from model.identified_object import IdentifiedObject
class TeamMember(IdentifiedObject):

    def __init__(self, oid, name, email):
        # initialization method that sets the oid, name and email properties as specified in the arguments (note: should call superclass constructor)
        super().__init__(oid)
        self._name = name
        self._email = email

    @property
    def name(self):
        #[prop]
        return self._name
    @name.setter
    def name(self, new_name):
        # [prop]
        self._name = new_name
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email




    def send_email(self, emailer, subject, message):
        # use the emailer argument to send an email to to this member
        emailer.send_plain_email([self.email], subject, message)

    def __str__(self):
        # return a string like the following: "Name<Email>"
        return f"{self.name}<{self.email}>"





