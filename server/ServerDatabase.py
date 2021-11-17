from UserInfo import UserInfo
from Message import Message
from PublicInfo import PublicInfo


class ServerDatabase:

    def __init__(self):
        """Constructs an initially empty server database"""
        self.__data: dict[str, UserInfo] = dict()

    def add_user(self, username: str, password: str):
        """Creates a new entry for the specified username with the specified password.
        If an entry for that username already exists, raises an exception."""

        # if the user already exists, raise an exception
        if self.user_exists(username):
            raise ServerDatabaseException("User already exists in server")

        # create a new UserInfo object for the user, set status to online by default
        new_user_info = UserInfo(username, password)
        new_user_info.set_public_info(PublicInfo(status_tag=PublicInfo.ONLINE))
        new_user_info.get_flags()['number_of_new_messages'] = 0

        # create a record for this user with the UserInfo object
        self.__data[username] = new_user_info

        # set the status change flags
        self.set_status_change_flags()

    def delete_user(self, username: str):
        """Deletes the entry in the server database for the specified user. If the
        username is not in the database, raises an exception"""

        # if the user does not exist, raise an exception
        if not self.user_exists(username):
            raise ServerDatabaseException("Attempting to delete non-existant user")

        # remove the user record from the database
        self.__data.pop(username)

        # set the status change flags
        self.set_status_change_flags()

    def get_user_info(self, username: str) -> UserInfo:
        """Returns the entire UserInfo object corresponding to the
        specified user. If none exists, returns None"""

        # if the user does not exist in the server, raise an exception
        if not self.user_exists(username):
            raise ServerDatabaseException("No record for user " + username)

        return self.__data.get(username)

    def get_server_public_info(self, username: str) -> dict[str, PublicInfo]:
        """Returns a the public information of each user in the form of
        a dictionary {username: status_info} if the specified user has their status change
         flag set. If the flag is not set (indicating no changes to the server status since
         last update) returns None."""

        # if the user does not exist in the server, raise an exception
        if not self.user_exists(username):
            raise ServerDatabaseException("No record for user " + username)

        # check if the user's info has a status change flag
        if self.get_user_info(username).get_flags().get('status_change'):

            # make a dictionary of public info objects
            public_info_dict = dict()
            for other_username in self.__data:
                public_info_dict[other_username] = self.get_user_info(other_username).get_public_info()

            # set the status change flag to false, indicating that they received the status update
            self.get_user_info(username).get_flags()['status_change'] = False

            # return the dictionary
            return public_info_dict

        # if the flag is not set, return None.
        else:
            return None

    def get_new_messages(self, username: str) -> list[Message]:
        """Returns a (possibly empty) list of messages which have been received by the specified
        user since the last time new messages were obtained."""

        # if the user does not exist in the server, raise an exception
        if not self.user_exists(username):
            raise ServerDatabaseException("No record for user " + username)

        # get the user's inbox and number of unread messages
        inbox = self.get_user_info(username).get_inbox()
        number_unread = self.get_user_info(username).get_flags()['number_of_new_messages']

        # get the unread messages
        message_list = []
        if number_unread > 0:
            message_list = inbox[-number_unread:]

        # set the number of new messages flag back to 0
        self.get_user_info(username).get_flags()['number_of_new_messages'] = 0

        return message_list

    def add_message(self, m: Message):
        """Adds the specified message to the outbox of the sender and the inbox of all the
        recipients"""

        # check that the sender username is valid
        sender = m.get_sender()
        if not self.user_exists(sender):
            raise ServerDatabaseException('Sender ' + sender + ' does not exist in server')

        # check that the list of recipients is valid
        recipients = m.get_recipients()
        if not self.__users_exist(recipients):
            raise ServerDatabaseException('Unknown recipient for message')

        # add to the outbox of the sender
        sender_outbox = self.get_user_info(sender).get_outbox()
        sender_outbox.append(m)

        # add to the inbox of each recipient and increment their number_of_new_messages counter
        for recipient in recipients:
            recipient_user_info = self.get_user_info(recipient)
            recipient_user_info.get_inbox().append(m)
            recipient_user_info.get_flags()['number_of_new_messages'] = \
                recipient_user_info.get_flags()['number_of_new_messages'] + 1

    def set_public_info(self, username: str, public_info: PublicInfo):
        """Sets the public info of the specified user to the specified PublicInfo object"""

        # if the user does not exist in the server, raise an exception
        if not self.user_exists(username):
            raise ServerDatabaseException("No record for user " + username)

        # set the user's public info, set the status change flags to alert the other users
        self.get_user_info(username).set_public_info(public_info)
        self.set_status_change_flags()

    def authenticate_user(self, username: str, password: str) -> bool:
        """Returns true if the password matches the recorded password for the
        specified username"""

        # if the user does not exist in the server return false
        if not self.user_exists(username):
            return False

        return self.get_user_info(username).get_password() == password

    def user_exists(self, username: str) -> bool:
        """Returns true if and only if there is a record for the specified username
        in the database"""
        return username in self.__data

    def __users_exist(self, usernames: list[str]) -> bool:
        """Returns true if and only if there is a record for each of the specified usernames
        in the database"""
        users_exist = [self.user_exists(username) for username in usernames]
        return all(users_exist)

    def set_status_change_flags(self):
        """Sets the record of each user to contain a status change flag, which indicates
        that there was a change in the status of at least one member of the server, which
        should be updated upon the next refresh cycle."""
        for user_info in self.__data.values():
            user_info.get_flags()["status_change"] = True


class ServerDatabaseException(Exception):
    pass

