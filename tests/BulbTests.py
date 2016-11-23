import mockito
import unittest
import Bulb

class BulbTests(unittest.TestCase):

    def setUp(self):
        self.home_sensor = mockito.mock()
        self.desk_sensor = mockito.mock()
        self.bed_sensor = mockito.mock()
        self.light_sensor = mockito.mock()

    def setReturnValues(self, bools):
        mockito.when(self.home_sensor).isHome().thenReturn(bools[0])
        mockito.when(self.desk_sensor).isAround().thenReturn(bools[1])
        mockito.when(self.bed_sensor).isAround().thenReturn(bools[2])
        mockito.when(self.light_sensor).isOn().thenReturn(bools[3])

    def test_kitchenLampWastedNotAround(self):
        self.setReturnValues((True, True, False, True))

        bulb = Bulb.Bulb('Kitchen',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.kitchenLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = True, Bulb.BULB_STATES.NOT_AROUND

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_kitchenLampWastedInBed(self):
        self.setReturnValues((True, False, True, True))

        bulb = Bulb.Bulb('Kitchen', self.light_sensor, [self.desk_sensor, self.bed_sensor], self.home_sensor,
                         Bulb.kitchenLampWasted)
        result0, result1 = bulb.isWasted()

        expected0, expected1 = True, Bulb.BULB_STATES.IN_BED

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_kitchenLampWastedNotHome(self):
        self.setReturnValues((False, False, True, True))

        bulb = Bulb.Bulb('Kitchen', self.light_sensor, [self.desk_sensor, self.bed_sensor], self.home_sensor,
                         Bulb.kitchenLampWasted)
        result0, result1 = bulb.isWasted()

        expected0, expected1 = True, Bulb.BULB_STATES.NOT_HOME

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_kitchenLampNotWasted(self):
        self.setReturnValues((True, False, True, False))

        bulb = Bulb.Bulb('Kitchen', self.light_sensor, [self.desk_sensor, self.bed_sensor], self.home_sensor,
                         Bulb.kitchenLampWasted)
        result0, result1 = bulb.isWasted()

        expected0, expected1 = False, Bulb.BULB_STATES.OFF

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_deskLampWastedNotAround(self):
        self.setReturnValues((True, False, False, True))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.deskLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = True, Bulb.BULB_STATES.NOT_AROUND

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_deskLampWastedNotHome(self):
        self.setReturnValues((False, False, False, True))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.deskLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = True, Bulb.BULB_STATES.NOT_HOME

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_deskLampNotWasted(self):
        self.setReturnValues((True, True, False, True))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.deskLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = False, Bulb.BULB_STATES.NOT_WASTED

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_deskLampOff(self):
        self.setReturnValues((True, True, False, False))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.deskLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = False, Bulb.BULB_STATES.OFF

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_deskLampWastedNotAround(self):
        self.setReturnValues((True, True, False, True))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.bedroomLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = True, Bulb.BULB_STATES.NOT_AROUND

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_deskLampWastedNotHome(self):
        self.setReturnValues((False, True, False, True))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.bedroomLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = True, Bulb.BULB_STATES.NOT_HOME

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)

    def test_bedroomLampOff(self):
        self.setReturnValues((True, True, False, False))

        bulb = Bulb.Bulb('Desk',self.light_sensor,[self.desk_sensor,self.bed_sensor],self.home_sensor,Bulb.bedroomLampWasted)
        result0, result1 = bulb.isWasted()
        expected0,expected1 = False, Bulb.BULB_STATES.OFF

        self.assertEqual(result0, expected0)
        self.assertEqual(result1, expected1)