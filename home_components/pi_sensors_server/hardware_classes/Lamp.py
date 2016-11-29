from Arduino_sensors_slave import Arduino_sensors_slave

class Lamp:
    def __init__(self, arduino, lamp_index, threshold):
        self.arduino = arduino
        self.lamp_index = lamp_index
        self.threshold = threshold

    def is_on(self):
        value = self.arduino.get_sensor_value(self.lamp_index)
        return value > self.threshold