class DuplicateEmail(Exception):
    """
    Exception raised when attempting to add a duplicate email.

    This exception is raised when attempting to add an email address to a collection
    or database that already exists.
    """
    def __init__(self,email):
        """
        Initialize the DuplicateEmail exception.

        :param email: The email address that caused the duplication.
        """
        super().__init__(email)
        self.value = email

class DuplicateOid(Exception):
    def __int__(self, oid):
        super.__init__(oid)
        self.value = oid
