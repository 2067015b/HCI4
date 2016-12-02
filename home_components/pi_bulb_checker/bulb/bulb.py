from bulb_states import BulbStates


class Bulb(object):
    """Class to contain the set of rules of around sensors"""

    def __init__(self, name, light_sensor, presence_sensors, home_sensor, wastage_function):
        self.name = name
        self.light_sensor = light_sensor
        self.presence_sensors = presence_sensors
        self.home_sensor = home_sensor
        self.wastage_function = wastage_function

    def is_wasted(self, *args):
        return self.wastage_function(self, *args)

    # Actual function implementations for the given lights

    def kitchen_lamp_wasted(self):
        desk_sensor = self.presence_sensors[0]
        bed_sensor = self.presence_sensors[1]

        if not self.light_sensor.isOn():
            return False, BulbStates.OFF
        elif not self.home_sensor.isHome():
            return True, BulbStates.NOT_HOME
        elif desk_sensor.isAround():
            return True, BulbStates.NOT_AROUND
        elif bed_sensor.isAround():
            return True, BulbStates.IN_BED
        else:
            return False, BulbStates.NOT_WASTED

    def desk_lamp_wasted(self):
        desk_sensor = self.presence_sensors[0]
        bed_sensor = self.presence_sensors[1]

        if not self.light_sensor.isOn():
            return False, BulbStates.OFF
        elif not self.home_sensor.isHome():
            return True, BulbStates.NOT_HOME
        elif desk_sensor.isAround():
            return False, BulbStates.NOT_WASTED
        elif bed_sensor.isAround():
            return True, BulbStates.IN_BED
        else:
            return True, BulbStates.NOT_AROUND

    def bedroom_lamp_wasted(self):
        desk_sensor = self.presence_sensors[0]
        bed_sensor = self.presence_sensors[1]
        if not self.light_sensor.isOn():
            return False, BulbStates.OFF
        elif not self.home_sensor.isHome():
            return True, BulbStates.NOT_HOME
        elif desk_sensor.isAround():
            return True, BulbStates.NOT_AROUND
        elif bed_sensor.isAround():
            return True, BulbStates.IN_BED
        else:
            return False, BulbStates.NOT_WASTED
