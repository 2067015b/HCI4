from bottle import *
from hardware_classes import *

arduino = ArduinoSensorsSlave(0x03)

lamp_sensors = [
    Lamp(arduino, 0)
]

presence_sensors = [
    PresenceAwareFurniture(arduino, 0)
]


@route('/lamp-sensor/<lamp_sensor_index>')
def get_lamp_state(lamp_sensor_index):
    return str(lamp_sensors[int(lamp_sensor_index)].is_on())


@route('/presence-sensor/<presence_sensor_index>')
def get_lamp_state(presence_sensor_index):
    return str(presence_sensors[int(presence_sensor_index)].is_around())

# This actually spins up the server and it starts listening. To listen on 0.0.0.0 you might need root privileges
run(host='0.0.0.0', port=8666, debug=True)
