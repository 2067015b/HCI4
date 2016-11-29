from bottle import *
from hardware_classes import *

arduino = ArduinoSensorsSlave(0x03)

lamps = {
    "deskLamp": Lamp(arduino, 0)
}

furnitures = {
    "desk": PresenceAwareFurniture(arduino, 0)
}


@route('/lamp/<lamp_name>')
def get_lamp_state(lamp_name):
    return lamps[lamp_name].is_on()


@route('/furniture/<furniture_name>')
def get_lamp_state(furniture_name):
    return furnitures[furniture_name].is_around()

# This actually spins up the server and it starts listening. To listen on 0.0.0.0 you might need root privileges
run(host='0.0.0.0', port=8666, debug=True)
