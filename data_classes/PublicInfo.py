

class PublicInfo:

    ONLINE = 0
    AWAY = 1
    BUSY = 2
    OFFLINE = 3
    CUSTOM = 4

    def __init__(self, status_tag: int = None, status_text: str = None, ):
        self.__status_tag = status_tag
        self.__status_text = status_text
        self.__groups = dict()

    def get_status_tag(self) -> int:
        return self.__status_tag

    def get_status_text(self):
        return self.__status_text

    def add_group(self, name: str, members: list[str]):
        self.__groups[name] = members

    def get_groups(self):
        return self.__groups
