from data_classes.UserInfo import UserInfo
from data_classes.Message import Message
from data_classes.PublicInfo import PublicInfo


class ClientDatabase:

    def __init__(self, username: str, password: str):
        self.__personal_info = UserInfo(username, password)
        self.__server_public_info = dict()

    def add_message(self, m: Message):
        """Adds the specified message to this user's database in the appropriate mailbox"""
        if m.get_sender() == self.__personal_info.get_username():
            self.get_outbox().append(m)
        elif self.__personal_info.get_username in m.get_recipients():
            self.get_inbox().append(m)
        else:
            raise ValueError('Either sender or receiver did not match this user record')

    def delete_message(self, m: Message):
        """Deletes this message from the appropriate mailbox. If it does not exist in the mailbox,
        a ValueError is raised."""
        if m in self.get_inbox():
            self.get_inbox().remove(m)
        if m in self.get_outbox():
            self.get_outbox().remove(m)

    def get_inbox(self) -> list[Message]:
        """Returns the inbox for this user's database"""
        return self.__personal_info.get_inbox()

    def get_outbox(self) -> list[Message]:
        """Returns the outbox for this user's database"""
        return self.__personal_info.get_outbox()

    def get_user_info(self) -> UserInfo:
        """Returns the UserInfo object containing this user's personal info in the database"""
        return self.__personal_info

    def set_user_info(self, user_info: UserInfo):
        """Sets the UserInfo object containing this user's personal info to the specified UserInfo
        object"""
        self.__personal_info = user_info

    def get_public_info(self):
        """Returns this user's PublicInfo object from the database"""
        return self.__personal_info.get_public_info()

    def set_public_info(self, public_info: PublicInfo):
        """Sets this user's PublicInfo to the specified PublicInfo object in the database"""
        self.__personal_info.set_public_info(public_info)

    def get_server_public_info(self) -> dict[PublicInfo]:
        """Returns the server public info record as a dictionary of PublicInfo objects keyed by username"""
        return self.__server_public_info

    def set_server_public_info(self, server_public_info: dict[PublicInfo]):
        """Sets the server public info record to the specified dictionary of PublicInfo objects keyed by
        username"""
        self.__server_public_info = server_public_info