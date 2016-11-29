class LightSensor:
    def __init__(self, arduino, light_sensor_index):
        self.arduino = arduino
        self.light_sensor_index = light_sensor_index

    def is_on(self):
        try:
            return self.arduino.get_light_sensor_value(self.light_sensor_index) == 1
        except:
            # if we somehow fail to read from the sensor, just say the light is off
            return False
