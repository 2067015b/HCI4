import FBPoster

class Shamer(object):

    def __init__(self,user_token):
        self.token = user_token
        self.FBPoster = FBPoster(user_token)
        self.TwitterPoster = None

    def shame_user(self, data = {}):
        ''' Decides on what to post, possibly aggregates several posts into one.'''
        pass

    def shame_for_sleeping(self, length, period=1):
        ''' Posts on user's wall because of leaving the lights on while sleeping. '''
        pass

    def shame_not_home(self, length, period=1):
        ''' Posts on user's wall because of leaving the lights on after leaving the home. '''
        pass

    def shame_for_wasting(self, length, period=1):
        ''' Posts on user's wall because of leaving the lights on while not being around. '''
        pass


class Analyzer(object):

    def __init__(self,server):
        self.DBserver = server
        self.user = self.DBserver.get_user()


    def retrieve_users_datapoints(self, days = 1):
        ''' Queries the database and returns a list of datapoints in the given timerange'''
        pass

    def run_bulb_analysis(self,days = 1):
        ''' Returns a dictionary with keys being the type of wasting/non-wasting and values being the time '''
        pass

    def run_analysis(self,days = 1):
        '''Analyze all the user's bulbs, return a dictionary referenced by the name of the bulb,
        containing the reason for shaming and the period over which it was wasted.
        Returns an empty dictionary if there's no reason to shame. '''
        pass