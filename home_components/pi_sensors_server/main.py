import time
from hardware_classes import *

arduino = Arduino_sensors_slave(0x03)
desk_lamp = Lamp(arduino, 0, 512)

while True:
    print "Desk lamp is %s" % ("on" if desk_lamp.is_on() else "off")
    time.sleep(1)