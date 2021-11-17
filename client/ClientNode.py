from StorageUtility import StorageUtility
from ClientDatabase import ClientDatabase
from ServerConnection import ServerConnection
from Message import Message
from PublicInfo import PublicInfo
from UserInfo import UserInfo
from threading import Thread, Event


class ClientNode:

    def __init__(self, host_address: str, username: str, password: str):
        """Initializes the data fields for the ClientNode object and sets
        the username and password fields"""
        self.__host_address = host_address
        self.__username = username
        self.__password = password
        self.__database: ClientDatabase = None
        self.__server_connection: ServerConnection = None
        self.__on_new_messages_received = lambda messages: None
        self.__on_new_server_public_info = lambda public_info: None
        self.__storage_utility = StorageUtility(f'{username}_client_database.txt')
        self.__is_online = False
        self.__autorefresh_on = False

    def login(self):
        """Sets up the ClientNode by attempting to load from an existing saved database
        or attempting to restore user information from the server. Assumes that there is an
        account on the server corresponding to this user. Raises an exception if the login fails"""

        # create a ServerConnection object
        if self.__server_connection is None:
            self.__server_connection = ServerConnection(self.__host_address, self.__username, self.__password)

        # attempt to log in the user
        response = self.__server_connection.login_user()
        if response != 'success':
            return False

        # set the online flag
        self.__is_online = True

        # attempt to load from a save file. If unsuccessful, restore from server:
        db = self.__storage_utility.load()
        if db is not None:
            self.__database = db
        else:
            self.__database = ClientDatabase(self.__username, self.__password)
            self.restore_user_info()
            self.__storage_utility.save(self.__database)

        # begin autosaving the database at the file path every 5 minutes
        self.__storage_utility.start_autosave(self.__database, timespan=300)

        # begin refreshing every 5 seconds
        self.start_autorefresh(timeout=5)

        return True

    def register_user(self):
        """Registers a new account for this user with the server and sets up a database to store
        this user's info on the local computer. Returns True if successful and False otherwise"""

        # create a ServerConnection object
        self.__server_connection = ServerConnection(self.__host_address, self.__username, self.__password)

        # register this user to the server
        response = self.__server_connection.register_new_user()
        if response != 'success':
            return False
        else:
            return True

    def logout(self):
        """Logs the user out by changing their status to offline in the server and sets the is_online flag
        to false"""

        # change public info to offline
        public_info = PublicInfo(status_tag=PublicInfo.OFFLINE)
        self.set_user_public_info(public_info)

        # change online flag to false
        self.__is_online = False

        # stop autosaving
        self.__storage_utility.stop_autosave()
        self.__storage_utility.save(self.__database)

        # stop autorefreshing()
        self.stop_autorefresh()

        return True

    def set_on_new_messages_received(self, target):
        """sets the specified target function to be performed on a list of new messages whenever
        new messages are received. The target function should accept a list of Message objects as an argument"""
        if self.__is_online:
            raise ClientNodeException('This change cannot be made while the node is online')
        self.__on_new_messages_received = target

    def set_on_new_server_public_info(self, target):
        """sets the specified target function to be performed on a dictionary of public_info whenever
        new server public information is received. The target function should accept a dictionary of PublicInfo
        objects keyed by username"""
        if self.__is_online:
            raise ClientNodeException('This change cannot be made while the node is online')
        self.__on_new_server_public_info = target

    def get_inbox(self):
        """Returns the user's inbox"""
        self.__assert_online()
        return self.__database.get_inbox()

    def get_outbox(self):
        """Returns the user's outbox"""
        self.__assert_online()
        return self.__database.get_outbox()

    def send_message(self, m: Message):
        """Sends the message to the server and updates the user's database with the message.
        returns True if successful and false otherwise"""
        self.__assert_online()

        response = self.__server_connection.send_message(m)
        if not response == 'success':
            print(response)
            return False

        try:
            self.__database.add_message(m)
        except ValueError:
            return False

        return True

    def delete_message(self, m: Message):
        """Deletes the specified message from the client database"""
        self.__assert_online()
        self.__database.delete_message(m)
        return True

    def get_user_public_info(self):
        """Returns the public info object for this user"""
        return self.__database.get_public_info()

    def set_user_public_info(self, p: PublicInfo):
        """Sends the public_info object to the server and updates the user's database
        with the public_info object. Returns true if successful and False otherwise"""
        self.__assert_online()

        response = self.__server_connection.update_public_info(p)
        if not response == 'success':
            return False

        try:
            self.__database.set_public_info(p)
        except ValueError:
            return False

        return True

    def get_server_public_info(self):
        """Gets the server public info from the database and returns it."""
        self.__assert_online()

        return self.__database.get_server_public_info()

    def get_user_list(self):
        """Returns a list of usernames registered on the server"""
        self.__assert_online()

        return list(self.get_server_public_info().keys())

    def start_autorefresh(self, timeout: int = 30):
        """Begins automatically refreshing the connection with the server at the interval
        of time specified by timeout (seconds)"""
        self.__assert_online()
        self.__autorefresh_on = True
        Thread(target=self.__autorefresh_loop, args=(timeout,), daemon=True).start()

    def stop_autorefresh(self):
        """Stops the autorefresh cycle"""
        self.__autorefresh_on = False

    def refresh(self):
        """Refreshes the client node by requesting new messages and new server public info from
        the server. If any is received, it handles it updating the database and calling the
        on_new_messages_received and on_new_public_server_info functions"""
        self.__assert_online()

        # get new messages
        messages = self.__server_connection.get_new_messages()

        # if there are any new messages, add them to database and process them
        if len(messages) > 0:
            self.get_inbox().extend(messages)
            self.__on_new_messages_received(messages)

        # get new server public info
        server_public_info = self.__server_connection.get_server_public_info()

        # if server public info is not None, update the database and process the changes
        if server_public_info is not None:
            self.__database.set_server_public_info(server_public_info)
            self.__on_new_server_public_info(server_public_info)

    def __autorefresh_loop(self, timeout: int):
        """Refreshes the client node at the interval of time specified by the paramenter timeout (seconds)"""
        while self.__autorefresh_on:
            self.refresh()
            Event().wait(timeout)


    def restore_user_info(self):
        """Obtains the server's UserInfo object for this user and overwrites the database with this object.
        Effectively restores any messages that may have been deleted from the inbox or outbox of the user
        returns true if successful and false otherwise"""
        self.__assert_online()

        # get the userinfo object and save it to the database
        user_info = self.__server_connection.get_user_info()
        try:
            assert type(user_info) == UserInfo
        except AssertionError:
            return False
        self.__database.set_user_info(user_info)

        # get the server public info and save it to the database
        self.__server_connection.update_public_info(self.get_user_public_info())
        public_info = self.__server_connection.get_server_public_info()
        try:
            assert type(public_info) == dict
        except AssertionError:
            return False
        self.__database.set_server_public_info(public_info)

        return True

    def __assert_online(self):
        if not self.__is_online:
            raise ClientNodeException(f'Client node for user {self.__username} is offline')


class ClientNodeException(BaseException):
    pass