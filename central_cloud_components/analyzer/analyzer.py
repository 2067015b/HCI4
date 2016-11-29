import collections
from home_components import BulbStates
from central_cloud_components import DBManager

BulbStatistics = collections.namedtuple('BulbStatistics', BulbStates.get_all_states())

class Analyzer(object):

    def __init__(self):
        self.db = DBManager()


    def retrieve_users_bulbs(self, days = 1):
        '''Returns a list of distinct bulbs from the db that were logged in the past 'days' '''
        return self.db.get("USER").keys()

    def retrieve_bulbs_data(self, bulb, days = 1):
        ''' Queries the database and returns a namedtuple with a field for each state.
            The format is as follows BulbStatistics(OFF, NOT_HOME, NOT_AROUND, IN_BED, NOT_WASTED)'''
        bulb_data = self.db.get("USER")[bulb]
        return BulbStatistics(OFF=bulb_data[0], NOT_HOME=bulb_data[1], NOT_AROUND=bulb_data[2],
                              IN_BED=bulb_data[3], NOT_WASTED=bulb_data[4])

    def run_analysis(self,days = 1):
        '''Analyze all the user's bulbs, return a dictionary referenced by the name of the bulb,
        containing the namedtuple of values for each bulb state '''
        bulbs = self.retrieve_users_bulbs(days)
        bulb_statistics = {}
        for bulb in bulbs:
            bulb_statistics[bulb] = self.retrieve_bulbs_data(bulb, days)
        return bulb_statistics
