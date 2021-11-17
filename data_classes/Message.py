from datetime import datetime


class Message:
    """An object which represent a message which may be sent by users
    of StaffChat and stored in databases by the client and server programs"""

    def __init__(self, sender: str = None,
                 recipients: list[str] = None,
                 subject: str = 'no subject',
                 content: str = 'no content'):
        self.__sender = sender
        self.__recipients = recipients
        self.__subject = subject
        self.__content = content
        self.__datetime = datetime.now()

    def get_sender(self) -> str:
        return self.__sender

    def get_recipients(self) -> list[str]:
        return self.__recipients

    def get_subject(self) -> str:
        return self.__subject

    def get_content(self) -> str:
        return self.__content

    def get_datetime(self) -> datetime:
        return self.__datetime

    def __repr__(self):
        return "Message(sender: {0}, \nrecipients: {1},\nsubject: {2}, \ncontent: {3})\n".format(\
            self.__sender, repr(self.__recipients), self.__subject, self.__content)