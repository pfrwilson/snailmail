from flask import Flask, request
from ServerDatabase import ServerDatabase, ServerDatabaseException
from data_classes.Message import Message
from data_classes.PublicInfo import PublicInfo
import jsonpickle
from utils.StorageUtility import StorageUtility

class ServerMain:

    app: Flask = Flask('__name__')
    db: ServerDatabase = None

    @classmethod
    def main(cls):
        cls.setup_database()
        cls.route_functions()
        cls.app.run("0.0.0.0")

    @classmethod
    def setup_database(cls):

        # load the database (None if the file does not exist)
        storage_utility = StorageUtility('server_database.txt')

        cls.db = storage_utility.load()
        if cls.db is None:
            cls.db = ServerDatabase()

        # begin autosaving the database
        storage_utility.start_autosave(cls.db, timespan=10)

    @classmethod
    def route_functions(cls):
        """Routes the functions to manipulate the server database to the appropriate
        url requests. """

        app = cls.app
        db = cls.db

        @app.route('/new_user/', methods = ['POST'])
        def new_user():
            """Creates a database entry for the new user with the specified name
            and password, if one does not exist. Returns "success" if the successful
            and 'failure: _reason_for_failure_ otherwise.
            REQUEST FORM: {"username": username,
                           "password": password}"""

            try:
                username = request.form['username']
                password = request.form['password']
            except:
                return "failure: bad form"
            try:
                db.add_user(username, password)
                return "success"
            except ServerDatabaseException as e:
                return "failure: user already exists in system"

        @app.route('/login/', methods=['POST'])
        def login_user():
            """If the request form contains a valid username and password, logs in the user
            by changing their status to 'Online' and returns the respons 'success'. Otherwise,
            returns the response 'failure'
            REQUEST FORM: {"username": username,
                           "password": password}"""

            try:
                username = request.form['username']
                password = request.form['password']
            except:
                return "failure: bad request form"

            if db.authenticate_user(username, password):
                public_info = PublicInfo(status_tag=PublicInfo.ONLINE)
                db.set_public_info(username, public_info)
                return 'success'

            else:
                return 'failure: login unsuccessful'

        @app.route('/get_server_public_info/', methods=['GET'])
        def get_server_public_info():
            """Gets public info for the server for the requesting user if there have been any changes
            to the public info since the last check-in.
            REQUEST FORM: {"username": username,
                           "password": password}"""
            try:
                username = request.form['username']
                password = request.form['password']
            except:
                return "failure: bad request form"

            if not (db.user_exists(username) and db.authenticate_user(username, password)):
                return "failure: user does not exist or passwords do not match"
            try:
                info = db.get_server_public_info(username)
                return jsonpickle.encode(info)
            except:
                return "failure: unknown server error"

        @app.route('/get_new_messages/', methods=['GET'])
        def get_new_messages():
            """Gets any new messages available for the requesting user.
            REQUEST FORM: {"username": username,
                           "password": password}"""
            try:
                username = request.form['username']
                password = request.form['password']
            except:
                return 'failure: bad request form'

            if not(db.user_exists(username) and db.authenticate_user(username, password)):
                return 'failure: user does not exist or passwords do not match'

            try:
                messages = db.get_new_messages(username)
                return jsonpickle.encode(messages)
            except:
                return 'failure: unknown server error'

        @app.route('/get_user_info/', methods=['GET'])
        def get_user_info():
            """Returns the entire user info object stored in the database for the requesting user.
            REQUEST FORM: {"username": username,
                           "password": password}"""

            try:
                username = request.form['username']
                password = request.form['password']
            except:
                return 'failure: bad request form'

            if not (db.user_exists(username) and db.authenticate_user(username, password)):
                return 'failure: user does not exist or passwords do not match'

            try:
                user_info = db.get_user_info(username)
                return jsonpickle.encode(user_info)
            except:
                return 'failure: unknown server error'

        # send_message
        @app.route('/send_message/', methods=['POST'])
        def send_message():
            """Sends the message from the posting user to the server database.
            REQUEST FORM: {"username": username,
                           "password": password
                           "message": message <- jsonpickle-encoded string}"""

            try:
                username = request.form['username']
                password = request.form['password']
                message = jsonpickle.decode(request.form['message'])
                assert type(message) == Message
            except:
                return 'failure: bad request form'

            if not (db.authenticate_user(username, password)):
                return 'failure: username and password do not match'

            if not message.get_sender() == username:
                return 'failure: username does not match sender'

            try:
                db.add_message(message)
                return 'success'
            except:
                return 'failure: error adding message to server'

        @app.route('/update_public_info/', methods=['POST'])
        def update_public_info():
            """Updates the requesting user's public info with the public info included in the
            request form.
            REQUEST FORM: {"username": username,
                           "password": password
                           "public_info": PublicInfo <- jsonpickle-encoded string}"""

            try:
                username = request.form['username']
                password = request.form['password']
                public_info = jsonpickle.decode(request.form['public_info'])
                assert type(public_info) == PublicInfo
            except:
                return 'failure: bad request form'

            if not (db.user_exists(username) and db.authenticate_user(username, password)):
                return 'failure: username does not exist or password does not match'

            try:
                db.set_public_info(username, public_info)
                return 'success'
            except:
                return 'failure: unknown server error'


if __name__ == '__main__':
    ServerMain.main()


