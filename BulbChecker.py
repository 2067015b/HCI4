import datetime

class BulbChecker(object):

    def __init__(self, bulbs, server, user=None):
        self.server = server
        self.user = server.get_user() or user
        self.bulbs = bulbs

    def submit_datapoint(self, user, bulbName, reason):
        ''' Submits this datapoint into the db '''
        self.server.add_entry(user=user, bulb=bulbName, reason=reason, datetime=datetime.datetime.now())

    def check_bulbs(self):
        ''' Checks each bulb and submits the data if relevant '''
        for bulb in self.bulbs:
            wasted, reason = bulb.wastage_function()
            if not reason == 'OFF':
                self.submit_datapoint(self.user,bulb.name,reason)
