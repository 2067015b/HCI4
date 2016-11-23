import unittest
import main
import datetime
import access
import dbmanager

b_start = datetime.datetime(2016, 11, 19, 18, 00)
b_end = datetime.datetime(2016, 11, 19, 20, 00)
u_start = datetime.datetime(2016, 11, 19, 17, 00)
u_end = datetime.datetime(2016, 11, 19, 19, 00)
u1 = datetime.datetime(2016, 11, 19, 19, 30)
u2 = datetime.datetime(2016, 11, 19, 21, 00)


def session_tupple(start, end):
    return (datetime.datetime(2016, 11, 19, start[0], start[1]), datetime.datetime(2016, 11, 19, end[0], end[1]))

class BulbTests(unittest.TestCase):

    def setUp(self):
        self.bulb = main.Bulb(name = 'Desk', times_on=[(b_start,b_end)], user_near=[(u_start,u_end),(u1,u2)])

    def test_getStats_zero_hrs_wasted(self,days=7):
        # ARRANGE
        bulb_sessions = [session_tupple((21, 00), (23, 30)), session_tupple((18, 00), (19, 30))]
        desk_sessions = [session_tupple((21, 00), (23, 30)), session_tupple((18, 00), (19, 30))]
        bulb = main.Bulb("some-lamp-name", times_on=bulb_sessions, user_near=desk_sessions)

        # ACT
        obtainedStats = bulb.getStats(days=1)

        # ASSERT
        # assert on values of whatever you obtained from ACT part making sure they are correct
        expectedStats = [(datetime.timedelta(0, 5400), datetime.timedelta(0, 5400)),
                        (datetime.timedelta(0, 9000), datetime.timedelta(0, 9000))]
        self.assertEqual(expectedStats, obtainedStats, 'wrong stats returned when user was always nearby a lamp.')

    def test_getStats_day_bulb_on_no_user(self):
        # ARRANGE
        bulb_sessions = [session_tupple((21,00), (23,30)), session_tupple((18,00),(19,30))]
        desk_sessions = [session_tupple((20,00),(20,30))]
        bulb = main.Bulb("some-lamp-name", times_on=bulb_sessions, user_near=desk_sessions)

        # ACT
        obtainedStats = bulb.getStats(days=1)

        # ASSERT
        # assert on values of whatever you obtained from ACT part making sure they are correct
        expectedStats = [(datetime.timedelta(0, 5400), datetime.timedelta(0)), (datetime.timedelta(0, 9000), datetime.timedelta(0))]
        self.assertEqual(expectedStats,obtainedStats,'wrong stats returned when user was not nearby a lamp.')

    def test_getStats_day_user_arrived_earlier(self):
        # ARRANGE
        bulb_sessions = [session_tupple((21,00), (23,30))]
        desk_sessions = [session_tupple((20,00),(22,30))]
        bulb = main.Bulb("some-lamp-name", times_on=bulb_sessions, user_near=desk_sessions)

        # ACT
        obtainedStats = bulb.getStats(days=1)

        # ASSERT
        # assert on values of whatever you obtained from ACT part making sure they are correct
        expectedStats = [(datetime.timedelta(0, 9000), datetime.timedelta(0, 5400))]
        self.assertEqual(expectedStats,obtainedStats,'wrong stats returned when user arrived before switching a lamp on.')

    def test_getStats_day_user_left_later(self):
        # ARRANGE
        bulb_sessions = [session_tupple((21,00), (22,30))]
        desk_sessions = [session_tupple((20,00),(23,30))]
        bulb = main.Bulb("some-lamp-name", times_on=bulb_sessions, user_near=desk_sessions)

        # ACT
        obtainedStats = bulb.getStats(days=1)
        print obtainedStats

        # ASSERT
        # assert on values of whatever you obtained from ACT part making sure they are correct
        expectedStats = [(datetime.timedelta(0, 5400), datetime.timedelta(0, 5400))]
        self.assertEqual(expectedStats,obtainedStats,'wrong stats returned when user left after the lamp.')




class PostManagerTest(unittest.TestCase):

    def setUp(self):
        bulb = main.Bulb(name='Desk', times_on=[(b_start, b_end)], user_near=[(u_start, u_end)])
        self.user = dbmanager.DBManager().get('USER') or access.FBOAuth().authenticate_user()
        self.user.populate(bulbs = [bulb])


    def CheckAndPost(self):
        post_manager = main.FBPostManager(user = self.user)
        post_manager.checkAndPost(weekly=False)

if __name__ == '__main__':
    unittest.main()