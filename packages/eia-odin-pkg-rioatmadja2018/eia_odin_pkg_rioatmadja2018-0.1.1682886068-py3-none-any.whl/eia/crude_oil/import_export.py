#!/usr/bin/env python3
from eia.utils.browser import Browser
from eia.utils.constants import API_KEY, REGION, IMPORT_EXPORT_FACETS
from eia.utils.facets import get_facets
from typing import List, Dict

class CrudeOilImportAndExport(object):

    def __init__(self, frequency: str = "weekly"):
        self.frequency: str = frequency
        self.all_items: Dict=  {}
        self.visited: Dict = {}

    def get_weekly_petroleum_import_export(self, length: int = 5000):

        for state,series in IMPORT_EXPORT_FACETS.items():
            endpoint: str = f"https://api.eia.gov/v2/petroleum/move/wkly/data/?api_key={API_KEY}&frequency={self.frequency}&data[0]=value&facets[series][]={series}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length={length}"

            if not self.visited.get(state, {}):
                resp: Dict = Browser(endpoint=endpoint).parse_content().get('response').get('data')
                self.all_items[state] = resp
                self.visited[REGION.get(state)] = resp

            else:
                self.all_items[state] = self.visited.get(REGION.get(state))
    @property
    def get_all_data(self):
        return self.all_items
