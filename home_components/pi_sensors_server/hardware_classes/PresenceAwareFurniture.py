class PresenceAwareFurniture:
    def __init__(self, arduino, presence_sensor_index):
        self.arduino = arduino
        self.presence_sensor_index = presence_sensor_index

    def is_around(self):
        return self.arduino.get_presence_sensor_value(self.presence_sensor_index) == 1
