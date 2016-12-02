from bottle import *
from hardware_classes import *

arduino = ArduinoSensorsSlave(0x03)

light_sensors = [
    LightSensor(arduino, 0)
]

presence_sensors = [
    PresenceSensor(arduino, 0),
    PresenceSensor(arduino, 1)
]


@route('/light-sensor/<light_sensor_index>')
def get_light_sensor_state(light_sensor_index):
    return str(light_sensors[int(light_sensor_index)].is_on())


@route('/presence-sensor/<presence_sensor_index>')
def get_presence_sensor_state(presence_sensor_index):
    return str(presence_sensors[int(presence_sensor_index)].is_around())

# This actually spins up the server and it starts listening. To listen on 0.0.0.0 you might need root privileges
run(host='0.0.0.0', port=8666, debug=True)
