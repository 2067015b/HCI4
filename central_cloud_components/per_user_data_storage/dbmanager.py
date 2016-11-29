"""
Module that holds the class responsible for object persistency
"""
import pickle
import os

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_NAME = str(dir)+'\BulbStatistics.pk'

class DBManager(object):
    """
    Database manager class. It encapsulates operations over the pickle module and utility methods over the
    actual user. The objects are saved in a hash-map like data structure
    """

    def database(self):
        """
        returns the database representation
        """
        try:
            database_file = open(DATABASE_NAME, 'rb')
            database = pickle.load(database_file)
        except IOError:
            database_file = open(str(dir)+'\BulbStatistics.pk', 'wb')
            database = dict()
            pickle.dump(database, database_file)
            database_file.close()
            database_file = open(DATABASE_NAME, 'rb')
            database = pickle.load(database_file)
        return database

    def save(self, name, value):
        """
        Saves an object under a particular name
        """
        database = self.database()
        database[name] = value
        database_file = open(str(dir)+'\BulbStatistics.pk', 'wb')
        pickle.dump(database, database_file)
        database_file.close()

    def get(self, name):
        """
        Retrieves and returns an object stored under the name 'name'
        """
        database = self.database()
        try:
            return database[name]
        except KeyError:
            return {}

    def reset(self):
        '''Deletes the database file '''
        try:
            os.remove(DATABASE_NAME)
            return "Our data has been wiped."
        except:
            return "There is nothing to remove."
