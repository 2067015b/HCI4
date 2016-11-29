class Lamp:
    def __init__(self, arduino, lamp_index):
        self.arduino = arduino
        self.lamp_index = lamp_index

    def is_on(self):
        try:
            return self.arduino.get_lamp_sensor_value(self.lamp_index) == 1
        except:
            # if we somehow fail to read from the sensor, jsut say the light is off
            return False
