
'''Class that contains the set of rules around sensors'''
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
    # assumes self.presence_sensors = [desk_sensor, bed_sensor]
    if not self.light_sensor.isOn():
        return False, 'OFF'
    elif not self.home_sensor.isHome():
        return True, 'NOT_HOME'
    elif self.presence_sensors[0].isAround():
        return True, 'NOT_AROUND'
    elif self.presence_sensors[1].isAround():
        return True, 'IN_BED'
    else:
        return False,'NOT_WASTED'

def deskLampWasted(self):
    # assumes self.presence_sensors = [desk_sensor, bed_sensor]
    if not self.light_sensor.isOn():
        return False, 'OFF'
    elif not self.home_sensor.isHome():
        return True, 'NOT_HOME'
    elif self.presence_sensors[0].isAround():
        return False, 'NOT_WASTED'
    elif self.presence_sensors[1].isAround():
        return True, 'IN_BED'
    else:
        return True,'NOT_AROUND'

def bedroomLampWasted(self):
    # assumes self.presence_sensors = [desk_sensor, bed_sensor]
    if not self.light_sensor.isOn():
        return False, 'OFF'
    elif not self.home_sensor.isHome():
        return True, 'NOT_HOME'
    elif self.presence_sensors[0].isAround():
        return True, 'NOT_AROUND'
    elif self.presence_sensors[1].isAround():
        return True, 'IN_BED'
    else:
        return False, 'NOT_WASTED'



