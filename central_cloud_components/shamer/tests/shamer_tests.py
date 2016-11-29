import unittest
import collections
import mock
from .. import Shamer
from .. import BulbStates

BulbStatistics = collections.namedtuple('BulbStatistics', BulbStates.get_all_states_as_string())

class ShamerTests(unittest.TestCase):

    def test_format_post_one_bulb_day(self):
        #ARRANGE
        bulbs_to_shame = {'kitchen':{'reason':BulbStates.NOT_AROUND, 'period':340}}
        shamer = Shamer('user_token')

        #ACT
        result_message = shamer.format_post(bulbs_to_shame)

        #ASSERT
        self.assertEqual("Yesterday I left my kitchen lights on for 5 hours and 40 minutes while I wasn't around.",result_message)

    def test_format_post_more_bulbs_day(self):
        # ARRANGE
        bulbs_to_shame = {'kitchen': {'reason': BulbStates.NOT_AROUND, 'period': 340},
                          'Desk': {'reason':BulbStates.IN_BED, 'period': 230}}
        shamer = Shamer('user_token')

        # ACT
        result_message = shamer.format_post(bulbs_to_shame)

        # ASSERT
        self.assertEqual("Yesterday I went to sleep for 3 hours and 50 minutes and forgot to switch my desk lights off. "
                         "I also left my kitchen lights on for 5 hours and 40 minutes while I wasn't around.",
                         result_message)

    def test_format_post_one_bulb_week(self):
        # ARRANGE
        bulbs_to_shame = {'Desk': {'reason':BulbStates.IN_BED, 'period': 1230}}
        shamer = Shamer('user_token')

        # ACT
        result_message = shamer.format_post(bulbs_to_shame, days=7)

        # ASSERT
        self.assertEqual("Last week I went to sleep for 20 hours and 30 minutes and forgot to switch my desk lights off.",
                         result_message)

    def test_format_post_more_bulbs_week(self):
        # ARRANGE
        bulbs_to_shame = {'kitchen': {'reason': BulbStates.NOT_AROUND, 'period': 740},
                          'Desk': {'reason':BulbStates.NOT_HOME, 'period': 1130},
                          'bedroom': {'reason':BulbStates.NOT_HOME, 'period': 830}}
        shamer = Shamer('user_token')

        # ACT
        result_message = shamer.format_post(bulbs_to_shame, days=7)

        # ASSERT
        self.assertEqual("Last week I left my home for 32 hours and 40 minutes and didn't switch my bedroom and desk lights off. "
                         "I also left my kitchen lights on for 12 hours and 20 minutes while I wasn't around.",
                         result_message)

    @mock.patch('facebook_poster.FBPoster.post', return_value=True)
    def test_shame_user_do_post(self, poster_mock):
        #ARRANGE
        data ={'desk' : BulbStatistics(OFF=490, NOT_HOME=340, NOT_AROUND=130, IN_BED=6, NOT_WASTED=580),
               'bedroom' : BulbStatistics(OFF=490, NOT_HOME=34, NOT_AROUND=230, IN_BED=640, NOT_WASTED=560)
               }

        #ACT
        result =Shamer("user_token").shame_user(data=data)

        #ASSERT
        self.assertEqual(True, result)
        poster_mock.assert_called_with("Yesterday I went to sleep for 10 hours and 40 minutes and forgot to switch my bedroom lights off. "
                                        "I also left my home for 5 hours and 40 minutes and didn't switch my desk lights off.")

    @mock.patch('facebook_poster.FBPoster.post', return_value=True)
    def test_shame_user_do_not_post(self, poster_mock):
        # ARRANGE
        data = {'Kitchen': BulbStatistics(OFF=490, NOT_HOME=34, NOT_AROUND=130, IN_BED=64, NOT_WASTED=560)}

        # ACT
        Shamer("user_token").shame_user(data=data)

        # ASSERT
        self.assertEqual(0, poster_mock.call_count)
