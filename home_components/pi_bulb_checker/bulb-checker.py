import urllib2


class BulbChecker(object):
    def __init__(self, bulbs):
        self.bulbs = bulbs

    def submit_datapoint(self, bulbName, state):
        """ Submits this datapoint into the db """
        return urllib2.urlopen(
            "http://localhost:8555/submit-bulb-datapoint?bulbName=" + bulbName + "&state=" + str(state))

    def check_bulbs(self):
        """ Checks each bulb and submits the data. """
        for bulb in self.bulbs:
            wasted, state = bulb.wastage_function()
            self.submit_datapoint(bulb.name, state)
