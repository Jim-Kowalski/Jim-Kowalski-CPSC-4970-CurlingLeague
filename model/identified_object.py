
class IdentifiedObject:
    """
    A class representing an identified object.
    """
    @property
    def oid(self):
        """
        Property representing the object ID for this object.

        :return: The object ID.
        """
        # [r/o prop] -- the object id for this object
        return self._oid

    def __init__(self, oid):
        """
        Initializes an IdentifiedObject with the specified OID.

        :param oid: The object ID.
        """
        # initialization method that sets the oid property as specified by the argument
        self._oid = oid

    def __eq__(self, other):
        """
        Checks if two IdentifiedObjects are equal.

        Two IdentifiedObjects are equal if they have the same type and the same OID.

        :param other: The object to compare with.
        :return: True if the objects are equal, False otherwise.
        """
        # two IndentifiedObjects are equal if they have the same type and the same oid

        # ensure that the objects are of the same type
        if type(self) != type(other):
            return False
        # return whether the objects are the same object id
        return self.oid == other.oid

    def __hash__(self):
        """
        Returns the hash code based on the object's OID.

        :return: The hash code.
        """
        # return hash code based on object's oid
        return hash(self._oid)

