import requests

class BulbChecker(object):

    def __init__(self, bulbs):
        self.bulbs = bulbs

    def submit_datapoint(self, bulbName, state):
        ''' Submits this datapoint into the db '''
        return requests.post("http://localhost:8555/submit-bulb-datapoint", data={'bulbName': bulbName, 'state':state})


    def check_bulbs(self):
        ''' Checks each bulb and submits the data. '''
        for bulb in self.bulbs:
            wasted, state = bulb.wastage_function()
            self.submit_datapoint(bulb.name,state)