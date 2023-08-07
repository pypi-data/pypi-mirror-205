#!/usr/bin/env python3
from unittest import TestCase
from eia.crude_oil.stocks import CrudeOilStocks
class TestCrudeOilStocks(TestCase):

    def test_get_weekly_supply_estimates(self):

        stocks: CrudeOilStocks = CrudeOilStocks()
        stocks.get_weekly_supply_estimates(length=2)
        print(stocks.get_all_data)
        self.assertEqual(len(stocks.get_all_data), 3)
