
import smbus
import time

class Arduino_sensors_slave:
    COMMS_BUFFER_SIZE = 4
    COMMAND_GET = 0
    COMMAND_SET = 1

    def __init__(self, arduino_i2c_address):
        self.arduino_i2c_address = arduino_i2c_address
        self.bus = smbus.SMBus(1)

    def __writeArray(self, command, array):
        self.bus.write_i2c_block_data(self.arduino_i2c_address, command, array)

    def __readArray(self, command):
        return self.bus.read_i2c_block_data(
            self.arduino_i2c_address, 
            command, 
            Arduino_sensors_slave.COMMS_BUFFER_SIZE)

    def __send_command_with_data(self, command, sensor_index, value):
        high, low = divmod(value, 0x100)
        array_to_send = [sensor_index, high, low]
        self.bus.write_i2c_block_data(self.arduino_i2c_address, command, array_to_send)

    def get_sensor_value(self, sensor_index):
        self.__send_command_with_data(Arduino_sensors_slave.COMMAND_GET, 
                                      sensor_index, 
                                      0)

        response = self.__readArray(Arduino_sensors_slave.COMMAND_GET)
        value = response[2] << 8
        value |= response[3]
        return value
