class PresenceSensor:
    def __init__(self, arduino, presence_sensor_index):
        self.arduino = arduino
        self.presence_sensor_index = presence_sensor_index

    def is_around(self):
        try:
            return self.arduino.get_presence_sensor_value(self.presence_sensor_index) == 1
        except:
            # if we somehow fail to read from the sensor, just say person isn't around...
            return False
