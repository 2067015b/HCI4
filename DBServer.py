
class DBServer(object):
    def __init__(self, db_address, username, password):
        self.db_address = db_address
        self.username = username
        self.password = password

    def connect_to_db(self):
        ''' Creates a connection to the db '''
        pass

    def add_entry(self, user, bulb, datetime, reason):
        ''' Submits a record into the db '''
        pass

    def get_user(self):
        ''' Returns the name of the user from the db '''
        pass

    def get_user_token(self):
        '''Returns the user's token from the db '''
        pass

    def close_connection(self):
        pass