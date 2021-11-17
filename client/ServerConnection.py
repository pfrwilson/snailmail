import requests
import jsonpickle
from data_classes.Message import Message


class ServerConnection:

    def __init__(self, home_address: str, username:str, password:str):
        self.__home_address = home_address
        self.__username = username
        self.__password = password

    def register_new_user(self):
        """Attempts to add a user with this username and password to the server. Returns the
        server response"""
        form = {'username': self.__username, 'password': self.__password}
        r = requests.post(f'{self.__home_address}new_user/', data=form)
        return r.text

    def login_user(self):
        """Attempts to log in the user. Returns the server response"""
        form = {'username': self.__username, 'password': self.__password}
        r = requests.post(f'{self.__home_address}login/', data=form)
        return r.text

    def get_server_public_info(self):
        """Gets the public info from the server for this user, if any changes have been made since
        the last check-in"""
        form = {'username': self.__username, 'password': self.__password}
        r = requests.get(f'{self.__home_address}get_server_public_info/', data=form)

        server_public_info = jsonpickle.decode(r.text)
        return server_public_info

    def get_new_messages(self):
        """Gets any new message available to this user"""
        form = {'username': self.__username, 'password': self.__password}
        r = requests.get(f'{self.__home_address}get_new_messages/', data=form)

        messages = jsonpickle.decode(r.text)
        return messages

    def get_user_info(self):
        """Gets the entire UserInfo object maintained by the server for this user"""
        form = {'username': self.__username, 'password': self.__password}
        r = requests.get(f'{self.__home_address}get_user_info/', data=form)

        user_info = jsonpickle.decode(r.text)
        return user_info

    def send_message(self, message: Message):
        """Attempts to send the specified message to the server and returns the server response"""
        form = {'username': self.__username, 'password': self.__password, 'message': jsonpickle.encode(message)}
        r = requests.post(f'{self.__home_address}send_message/', data=form)
        return r.text

    def update_public_info(self, public_info):
        """Attempts to update the server with the specified public_info for the user and returns
        the server's response"""
        form = {'username': self.__username, 'password': self.__password, 'public_info': jsonpickle.encode(public_info)}
        r = requests.post(f'{self.__home_address}update_public_info/', data=form)
        return r.text

