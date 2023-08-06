#!/usr/bin/env python3
from unittest import TestCase
from eia.crude_oil.production import CrudeOilProduction

class TestCrudeOilProduction(TestCase):

    def test_monthly_production(self):
        crude_oil_production: 'CrudeOilProduction' = CrudeOilProduction()
        crude_oil_production.get_crude_oil_production()

        print("[ 11 ]", crude_oil_production.all_productions)
        self.assertEqual( len(crude_oil_production.all_productions.keys()), 6)

    def test_yearly_production(self):
        crude_oil_production: 'CrudeOilProduction' = CrudeOilProduction(frequency='annual')
        crude_oil_production.get_crude_oil_production()

        print("[ 18 ]", crude_oil_production.all_productions)
        self.assertEqual( len(crude_oil_production.all_productions.keys()), 6)