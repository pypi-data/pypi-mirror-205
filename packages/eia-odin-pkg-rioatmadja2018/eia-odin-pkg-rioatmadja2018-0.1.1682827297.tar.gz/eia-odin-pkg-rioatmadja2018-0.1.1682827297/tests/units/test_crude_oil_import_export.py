#!/usr/bin/env python3
from unittest import TestCase
from eia.crude_oil.import_export import CrudeOilImportAndExport
from eia.utils.constants import STATE
from eia.utils.facets import get_facets

class TestCrudeOilImportAndExport(TestCase):

    def test_get_weekly_petroleum_import_export(self):

        coie: 'CrudeOilImportAndExport' = CrudeOilImportAndExport()
        coie.get_weekly_petroleum_import_export(length=1)
        print("[ 12 ]", coie.get_all_data.keys() )
        self.assertEqual(len(coie.get_all_data.keys()), len(STATE) )