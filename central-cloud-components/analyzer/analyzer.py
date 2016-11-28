import collections
from .. import BulbStates

class Analyzer(object):

    def __init__(self,server):
        self.DBserver = server
        self.user = self.DBserver.get_user()
        BulbStatistics = collections.namedtuple('BulbStatistics', BulbStates.get_all_states_as_string())


    def retrieve_users_bulbs(self, days = 1):
        '''Returns a list of distinct bulbs from the db that were logged in the past 'days' '''
        # TODO: Implement this method given our db.
        pass

    def retrieve_and_sort_bulbs_data(self, bulb, days = 1):
        ''' Queries the database and returns a namedtuple with a field for each state.
            The format is as follows BulbStatistics(OFF, NOT_HOME, NOT_AROUND, IN_BED, NOT_WASTED)'''
        # TODO: Implement this method given our db.
        pass

    def run_analysis(self,days = 1):
        '''Analyze all the user's bulbs, return a dictionary referenced by the name of the bulb,
        containing the namedtuple of values for each bulb state '''
        bulbs = self.retrieve_users_bulbs(days)
        bulb_statistics = {}
        for bulb in bulbs:
            bulb_statistics[bulb] = self.retrieve_and_sort_bulbs_data(bulb, days)
        return bulb_statistics
