import mockito
import unittest
from .. import Bulb
from .. import BulbStates


class BulbTests(unittest.TestCase):
    def setUp(self):
        self.home_sensor = mockito.mock()
        self.desk_sensor = mockito.mock()
        self.bed_sensor = mockito.mock()
        self.light_sensor = mockito.mock()

    def set_fixed_sensor_readings(self, isHome, isAroundDesk, isAroundBed, isBulbOn):
        mockito.when(self.home_sensor).isHome().thenReturn(isHome)
        mockito.when(self.desk_sensor).isAround().thenReturn(isAroundDesk)
        mockito.when(self.bed_sensor).isAround().thenReturn(isAroundBed)
        mockito.when(self.light_sensor).isOn().thenReturn(isBulbOn)

    def test_kitchen_lamp_wastedNotAround(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=True,
                                       isAroundBed=False,
                                       isBulbOn=True)

        bulb = Bulb('Kitchen',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.kitchen_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = True, BulbStates.NOT_AROUND
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_kitchen_lamp_wastedInBed(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=False,
                                       isAroundBed=True,
                                       isBulbOn=True)

        bulb = Bulb('Kitchen',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.kitchen_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = True, BulbStates.IN_BED
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_kitchen_lamp_wastedNotHome(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=False,
                                       isAroundDesk=False,
                                       isAroundBed=True,
                                       isBulbOn=True)

        bulb = Bulb('Kitchen',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.kitchen_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        expected_is_wasted, expected_bulb_state = True, BulbStates.NOT_HOME
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_kitchenLampNotWasted(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=False,
                                       isAroundBed=True,
                                       isBulbOn=False)

        bulb = Bulb('Kitchen',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.kitchen_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = False, BulbStates.OFF
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_desk_lamp_wastedNotAround(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=False,
                                       isAroundBed=False,
                                       isBulbOn=True)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = True, BulbStates.NOT_AROUND
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_desk_lamp_wastedNotHome(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=False,
                                       isAroundDesk=False,
                                       isAroundBed=False,
                                       isBulbOn=True)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = True, BulbStates.NOT_HOME
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_deskLampNotWasted(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=True,
                                       isAroundBed=False,
                                       isBulbOn=True)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = False, BulbStates.NOT_WASTED
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_deskLampOff(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=True,
                                       isAroundBed=False,
                                       isBulbOn=False)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = False, BulbStates.OFF
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_desk_lamp_wastedNotAround(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=False,
                                       isAroundBed=False,
                                       isBulbOn=True)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = True, BulbStates.NOT_AROUND
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_desk_lamp_wastedNotHome(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=False,
                                       isAroundDesk=True,
                                       isAroundBed=False,
                                       isBulbOn=True)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = True, BulbStates.NOT_HOME
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)

    def test_bedroomLampOff(self):
        # ARRANGE
        self.set_fixed_sensor_readings(isHome=True,
                                       isAroundDesk=True,
                                       isAroundBed=False,
                                       isBulbOn=False)

        bulb = Bulb('Desk',
                    self.light_sensor,
                    [self.desk_sensor, self.bed_sensor],
                    self.home_sensor,
                    Bulb.desk_lamp_wasted)

        # ACT
        actual_is_wasted, actual_bulb_state = bulb.is_wasted()

        # ASSERT
        expected_is_wasted, expected_bulb_state = False, BulbStates.OFF
        self.assertEqual(actual_is_wasted, expected_is_wasted)
        self.assertEqual(actual_bulb_state, expected_bulb_state)
