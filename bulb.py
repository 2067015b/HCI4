
import datetime


class Bulb(object):

    def __init__(self,  name=None):
        self.name = name
        self.not_home_wasted = []
        self.not_present_wasted = []
        self.sleeping_wasted = []
        self.utilized = []
        # 3d array matrix[home][present][sleeping]
        self.matrix = [[[self.utilized for k in xrange(2)] for j in xrange(2)] for i in xrange(2)]

    def populate_matrix(self,not_home_wasted,not_present_wasted,sleeping_wasted):
        for triple in not_home_wasted:
            self.matrix [triple[0]][triple[1]][triple[2]] = self.not_home_wasted

        for triple in not_present_wasted:
            self.matrix [triple[0]][triple[1]][triple[2]] = self.not_present_wasted

        for triple in sleeping_wasted:
            self.matrix [triple[0]][triple[1]][triple[2]] = self.sleeping_wasted

    def get_sleep_stats(self,days=1):
        '''Returns the time in minutes that the lights were wasted because the person was asleep'''
        last_day = datetime.datetime.now() - datetime.timedelta(days= days+1)
        minutes = 0
        for entry in self.sleeping_wasted:
            if entry>=last_day:
                minutes+=1
        return minutes

    def get_non_presence_stats(self,days=1):
        '''Returns the time in minutes that the lights were wasted because the person was not around'''
        last_day = datetime.datetime.now() - datetime.timedelta(days= days+1)
        minutes = 0
        for entry in self.not_present_wasted:
            if entry>=last_day:
                minutes+=1
        return minutes

    def get_non_home_stats(self,days=1):
        '''Returns the time in minutes that the lights were wasted because the person was not at home'''
        last_day = datetime.datetime.now() - datetime.timedelta(days= days+1)
        minutes = 0
        for entry in self.not_home_wasted:
            if entry>=last_day:
                minutes+=1
        return minutes

    def get_utilisation_stats(self,days=1):
        '''Returns the time in minutes that the lights were not wasted'''
        last_day = datetime.datetime.now() - datetime.timedelta(days= days+1)
        minutes = 0
        for entry in self.utilized:
            if entry>=last_day:
                minutes+=1
        return minutes

    def log_stats(self,key):
        self.matrix[key[0]][key[1]][key[2]].append(datetime.datetime.now())

