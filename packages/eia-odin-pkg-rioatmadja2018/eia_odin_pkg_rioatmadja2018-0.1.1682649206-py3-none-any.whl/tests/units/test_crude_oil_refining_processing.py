from unittest import TestCase
from eia.crude_oil.refining_processing import CrudeOilRefinigAndProcessing
from eia.utils.constants import STATE

class TestCrudeOilRefinigAndProcessing(TestCase):

    def test_weekly_refing_and_processing(self):
        refing_processing: 'CrudeOilRefinigAndProcessing' = CrudeOilRefinigAndProcessing()
        refing_processing.get_crude_oil_refining_processing()
        print(refing_processing.get_all_productions.keys() )
        return self.assertEqual(len(refing_processing.get_all_productions.keys()), len(STATE))
