from data_classes.Message import Message
from data_classes.PublicInfo import PublicInfo


class UserInfo:

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        self.__inbox = list()
        self.__outbox = list()
        self.__public_info = PublicInfo()
        self.__flags = dict()

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_inbox(self) -> list[Message]:
        return self.__inbox

    def get_outbox(self) -> list[Message]:
        return self.__outbox

    def get_public_info(self) -> PublicInfo:
        return self.__public_info

    def set_public_info(self, public_info: PublicInfo):
        self.__public_info = public_info

    def get_flags(self):
        return self.__flags


