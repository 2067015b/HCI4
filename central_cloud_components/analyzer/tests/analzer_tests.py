import unittest
import mock
import mockito
import collections
from .. import Analyzer
from .. import BulbStates

BulbStatistics = collections.namedtuple('BulbStatistics', BulbStates.get_all_states_as_string())

class AnalyzerTests(unittest.TestCase):

    @mock.patch('Analyzer.retrieve_users_bulbs', return_value=["kitchen","desk","bedroom"])
    @mock.patch('Analyzer.retrieve_bulbs_data',
                return_value = BulbStatistics(OFF=490, NOT_HOME=34, NOT_AROUND=130, IN_BED=64, NOT_WASTED=560))
    def test_run_analysis(self, retrieve_bulbs_mock, retrieve_data_mock):
        #ARRANGE
        server = mockito.mock()
        mockito.when(server).get_user().thenReturn('user')
        analyzer = Analyzer(server)

        #ACT
        result = analyzer.run_analysis(1)

        #ASSERT
        expected = {"kitchen":BulbStatistics(OFF=490, NOT_HOME=34, NOT_AROUND=130, IN_BED=64, NOT_WASTED=560),
                    "desk":BulbStatistics(OFF=490, NOT_HOME=34, NOT_AROUND=130, IN_BED=64, NOT_WASTED=560),
                    "bedroom":BulbStatistics(OFF=490, NOT_HOME=34, NOT_AROUND=130, IN_BED=64, NOT_WASTED=560)
                    }
        self.assertEquals(result,expected)


    @mock.patch('Analyzer.retrieve_users_bulbs',
                return_value=[])
    def test_run_analysis_empty(self, retrieve_bulbs_mock):
        # ARRANGE
        server = mockito.mock()
        mockito.when(server).get_user().thenReturn('user')
        analyzer = Analyzer(server)

        # ACT
        result = analyzer.run_analysis(1)

        # ASSERT
        expected = {}
        self.assertEquals(result, expected)