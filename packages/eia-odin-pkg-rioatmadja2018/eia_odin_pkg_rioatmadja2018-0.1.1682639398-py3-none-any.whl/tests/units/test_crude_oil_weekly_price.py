#!/usr/bin/env python3
from unittest import TestCase
from eia.crude_oil.pricing import CrudeOilPrice

class TestCrudeOilPrice(TestCase):

    def test_weekly_price(self):
       crude_oil: 'CrudeOilPrice' = CrudeOilPrice()
       crude_oil.get_weekly_retail_price()
       print("[ 12 ]" , list(crude_oil.all_pricing.keys()) )
       return self.assertEqual(len(crude_oil.all_pricing), 9)

    def test_monthly_price(self):
       crude_oil: 'CrudeOilPrice' = CrudeOilPrice(frequency="monthly")
       crude_oil.get_weekly_retail_price()
       print("[ 18 ]" , list(crude_oil.all_pricing.keys()) )
       return self.assertEqual(len(crude_oil.all_pricing), 9)

    def test_yearly_price(self):
       crude_oil: 'CrudeOilPrice' = CrudeOilPrice(frequency="annual")
       crude_oil.get_weekly_retail_price()
       print("[ 24 ]" , list(crude_oil.all_pricing.keys()) )
       return self.assertEqual(len(crude_oil.all_pricing), 9)

