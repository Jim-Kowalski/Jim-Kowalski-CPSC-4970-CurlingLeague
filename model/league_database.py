import csv
import os
import pickle
from model.custom_exceptions import DuplicateOid
class LeagueDatabase():
    """
    A singleton class for managing leagues.
    """

    _sole_instance = None

    def __init__(self):
        """
        Initializes the LeagueDatabase instance.
        """
        self._last_oid = 0 #private variable holding the last id number that was supplied (see methods below)
        self._leagues = []


    @classmethod
    def instance(cls):
        """
        Returns the sole instance of this database, creating one if it doesn't exist yet.
        """
        # returns the sole instance of this database, creating one if it doesn't exist yet
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @property
    def leagues(self):
        """
        [r/o prop] -- list of the leagues being managed
        """
        # [r/o prop] -- list of the leagues being managed
        return self._leagues

    def add_league(self, league):
        """
         Adds the specified league to the database.

         :param league: The league to add.
         """
        # add the specified league to the leagues list.

        if league not in self.leagues:
            self.leagues.append(league)
        else:
            raise DuplicateOid(league.oid)

    def remove_league(self, league):
        """
        Removes the specified league from the database.
        If league is not in the leagues list, simply do nothing (not an error).

        :param league: The league to remove.
        """
        # remove the specified league from the leagues list.
        # If league is not in the leagues list, simply do
        # nothing (not an error).
        if league in self.leagues:
            self.leagues.remove(league)

    def find_free_league_oid(self):
        #gather the used oid's in the collection of leagues.
        used_oids = {league.oid for league in self._leagues}
        # Start with oid 1 and count up to the length of the number of leagues
        # in the list. If there are 4 leagues, and there are oid gaps, at least
        # one oid will be missing. So, the algorithm will return the missing oid.

        # If there are no gaps, we allow an additional couple of indexes
        # and will select the oid that exceeds the last known oid.
        for oid in range(1, len(self._leagues) + 2):
            if oid not in used_oids:
                return oid
        return None  # If no free oid is found



    def league_named(self, name):
        """
        Returns the league with the specified name.

        :param name: The name of the league to retrieve.
        :return: Returns a league object if the league is found, otherwise None.
        """
        for league in self.leagues:
            if league.name == name:
                return league
        return None

    def next_oid(self):
        """
       Increments _last_id and return its new value

       :return: The new value of _last_oid.
       """
        #increment _last_id and return its new value (used to generate oid's for your objects)
        self._last_oid += 1
        return self._last_oid

    def load(self, file_name):
        """
        Loads a LeagueDatabase from the specified file.
        If file_name does not exist or an error occurs when reading it, display an error message
        and loads the file from the backup (if it exists).

        :param file_name: The name of the file to load.
        """
        # loads a LeagueDatabase from the specified file and stores it in
        # _sole_instance.  If file_name does not exist or an error occurs
        # when reading it, display a console message (ugh, sorry, it would
        # be better to use the logging framework here but I don't want to
        # go into it) and load the file from the backup (if it exists).
        # See save() for information on the backup file.
        file_loaded = False
        try:
            with open(file_name, 'rb') as league_file:
                #self.__class__._sole_instance = pickle.load(league_file)
                loaded_instance = pickle.load(league_file)
                loaded_instance.__class__._sole_instance = loaded_instance
                # loaded_instance._leagues = loaded_instance._leagues  # Reassign _leagues
                file_loaded = True
        except FileNotFoundError:
            print(f"ERRROR! File Not Found! Could not load filename: {file_name}")
        except Exception as e:
            print(f"ERROR! - {e}")
        if not file_loaded:
            backup_file_name = file_name + ".backup"
            if os.path.exists(backup_file_name):
                self.load(backup_file_name)

    def save(self, file_name):
        """
        Saves this database on the specified file. Before saving, it checks if the file exists
        and if it does, renames it to file_name with ".backup" added.

        :param file_name: The name of the file to save.
        """
        # save this database on the specified file.  Before saving, check if
        # the file exists and if it does, rename it to file_name with
        # ".backup" added.
        try:
            # Rename the pre-existing file if it exists.
            if os.path.exists(file_name):
                backup_file_index = 0  # specifies an index for the filename
                backup_file_name = file_name + ".backup"
                filename_found = False  # indicates a suitable filename was found

                # The 'backup' filename will be indexed if it is already present
                if os.path.exists(backup_file_name):
                    while not filename_found:
                        filename_found = False  # indicates a suitable filename was found
                        backup_file_index += 1
                        backup_file_name = file_name + ".backup" + str(backup_file_index)
                        if not os.path.exists(backup_file_name):
                            filename_found = True
                os.rename(file_name, backup_file_name)

            # Open a new file to serialize the league database.
            with open(file_name, 'wb') as dump_file:
                pickle.dump(self.__class__._sole_instance, dump_file)

        except Exception as e:
            print(f"ERROR! - {e}")

    def load_backup(self, file_name):
        """
        Loads the backup file.

        :param file_name: The name of the file to load backup from.
        """
        backup_file = file_name + ".backup"
        try:
            with open(backup_file, 'rb') as file:
                self._sole_instance = pickle.load(file)
        except FileNotFoundError:
            print("Backup file not found.")
        except Exception as e:
            print(f"Error loading backup: {e}")


    def import_league_teams(self, league, file_name):
        """
        Loads the teams and team members in a league from a CSV formatted file.

        :param league: The league to load teams into.
        :param file_name: The name of the CSV file to import.
        """

        # load the teams and team members in a league from a CSV formatted file. (The Python
        # standard library has a nice CSV module Links to an external site.).
        # The file will contain three columns: team name, team member name, email.  The first
        # line of the file will be a "header" line and should be ignored.  The file will be
        # UTF-8 encoded and may contain non-ASCII text. Note that the first argument to this
        # method must be a league object, not the name of a league.  If an error occurs while
        # loading a league, display a message on the console.  Here is a sample file.
        try:
            with open(file_name, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # skip header
                for row in reader:
                    team_name, member_name, email = row
                    team = league.get_team_by_name(team_name)
                    if team:
                        team.add_member(member_name, email)
                    else:
                        print(f"Team '{team_name}' not found in league '{league.name}'.")
        except Exception as e:
            print(f"Error import_league_teams: {e}")

    def export_league_teams(self, league, file_name):
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
                for team in league.teams:
                    for member in team.members:
                        writer.writerow([team.name, member.name, member.email])
        except Exception as e:
            print(f"Error exporting league teams: {e}")

