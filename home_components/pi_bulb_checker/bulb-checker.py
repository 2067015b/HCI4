import urllib2

from time import gmtime, strftime, sleep

from home_components.pi_bulb_checker.bulb import Bulb
from home_components.pi_bulb_checker.bulb.home_sensor import HomeSensor
from home_components.pi_bulb_checker.bulb.light_sensor import LightSensor
from home_components.pi_bulb_checker.bulb.presence_sensor import PresenceSensor

SAMPLES_PER_MINUTE = 6


class BulbChecker(object):
    def __init__(self, bulbs):
        self.bulbs = bulbs

    @staticmethod
    def __submit_datapoint(bulb_name, state):
        """ Submits this datapoint into the db """
        return urllib2.urlopen(
            "http://localhost:8555/submit-bulb-datapoint?bulbName=" + bulb_name + "&state=" + str(state))

    def check_bulbs(self):
        """ Checks each bulb and submits the data. """
        for bulb in self.bulbs:
            wasted, state = bulb.wastage_function(bulb)
            print "%s: submitting data for bulb '%s'. It is %swasted" % (
                strftime("%H:%M:%S", gmtime()), bulb.name, '' if wasted else 'NOT ')
            self.__submit_datapoint(bulb.name, state)


if __name__ == "__main__":
    home_sensor = HomeSensor()

    desk_lamp_light_sensor = LightSensor("http://localhost:8666/light-sensor/0");
    desk_lamp_relevant_presence_sensors = [
        PresenceSensor("http://localhost:8666/presence-sensor/0"),  # desk
        PresenceSensor("http://localhost:8666/presence-sensor/1")   # bed
    ]
    desk_lamp = Bulb("deskLamp",
                     desk_lamp_light_sensor,
                     desk_lamp_relevant_presence_sensors,
                     home_sensor,
                     Bulb.desk_lamp_wasted)

    all_bulbs = [desk_lamp]

    checker = BulbChecker(all_bulbs)

    sleep_delay_in_s = 60 / SAMPLES_PER_MINUTE

    while True:
        checker.check_bulbs()
        sleep(sleep_delay_in_s)
