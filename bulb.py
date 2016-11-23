
# Since python 2.7 doesn't support enums,
class BULB_STATES:
    OFF, NOT_HOME, NOT_AROUND, IN_BED, NOT_WASTED = range(5)

'''Class to contain the set of rules of around sensors'''
class Bulb(object):

    def __init__(self,  name, lightSensor, presenceSensors, homeSensor, wastage_function):
        self.name = name
        self.light_sensor = lightSensor
        self.presence_sensors = presenceSensors
        self.home_sensor = homeSensor
        self.wastage_function = wastage_function


    def isWasted(self, *args):
        return self.wastage_function(self,*args)


# Actual function implementation for the given lights

def kitchenLampWasted(self):
    desk_sensor = self.presence_sensors[0]
    bed_sensor = self.presence_sensors[1]

    if not self.light_sensor.isOn():
        return False, BULB_STATES.OFF
    elif not self.home_sensor.isHome():
        return True, BULB_STATES.NOT_HOME
    elif desk_sensor.isAround():
        return True, BULB_STATES.NOT_AROUND
    elif bed_sensor.isAround():
        return True, BULB_STATES.IN_BED
    else:
        return False,BULB_STATES.NOT_WASTED

def deskLampWasted(self):
    desk_sensor = self.presence_sensors[0]
    bed_sensor = self.presence_sensors[1]

    if not self.light_sensor.isOn():
        return False, BULB_STATES.OFF
    elif not self.home_sensor.isHome():
        return True, BULB_STATES.NOT_HOME
    elif desk_sensor.isAround():
        return False, BULB_STATES.NOT_WASTED
    elif bed_sensor.isAround():
        return True, BULB_STATES.IN_BED
    else:
        return True,BULB_STATES.NOT_AROUND

def bedroomLampWasted(self):
    desk_sensor = self.presence_sensors[0]
    bed_sensor = self.presence_sensors[1]
    if not self.light_sensor.isOn():
        return False, BULB_STATES.OFF
    elif not self.home_sensor.isHome():
        return True, BULB_STATES.NOT_HOME
    elif desk_sensor.isAround():
        return True, BULB_STATES.NOT_AROUND
    elif bed_sensor.isAround():
        return True, BULB_STATES.IN_BED
    else:
        return False, BULB_STATES.NOT_WASTED



