import smbus
import time


class ArduinoSensorsSlave:
    COMMS_BUFFER_SIZE = 4
    COMMAND_GET_LIGHT_SENSOR = 0
    COMMAND_GET_PRESENCE_SENSOR = 1

    def __init__(self, arduino_i2c_address):
        self.arduino_i2c_address = arduino_i2c_address
        self.bus = smbus.SMBus(1)

    def __write_array(self, command, array):
        self.bus.write_i2c_block_data(self.arduino_i2c_address, command, array)

    def __read_array(self, command):
        return self.bus.read_i2c_block_data(
            self.arduino_i2c_address,
            command,
            ArduinoSensorsSlave.COMMS_BUFFER_SIZE)

    def __send_command_with_data(self, command, sensor_index, value):
        high, low = divmod(value, 0x100)
        array_to_send = [sensor_index, high, low]
        self.bus.write_i2c_block_data(self.arduino_i2c_address, command, array_to_send)

    def get_light_sensor_value(self, sensor_index):
        self.__send_command_with_data(ArduinoSensorsSlave.COMMAND_GET_LIGHT_SENSOR,
                                      sensor_index,
                                      0)

        response = self.__read_array(ArduinoSensorsSlave.COMMAND_GET_LIGHT_SENSOR)
        value = response[2] << 8
        value |= response[3]
        return value

    def get_presence_sensor_value(self, sensor_index):
        self.__send_command_with_data(ArduinoSensorsSlave.COMMAND_GET_PRESENCE_SENSOR,
                                      sensor_index,
                                      0)

        response = self.__read_array(ArduinoSensorsSlave.COMMAND_GET_PRESENCE_SENSOR)
        value = response[2] << 8
        value |= response[3]
        return value
