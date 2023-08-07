#!/usr/bin/env python3
from eia.utils.browser import Browser
from eia.utils.constants import API_KEY
from typing import List, Dict

class CrudeOilStocks(object):

    def __init__(self, frequency: str = "weekly"):
        self.all_data: List = []
        self.frequency: str = frequency

    def get_weekly_supply_estimates(self, length: int = 5000):

        endpoint: str = f"https://api.eia.gov/v2/petroleum/sum/sndw/data/?api_key={API_KEY}&frequency={self.frequency}&data[0]=value&facets[series][]=WTTSTUS1&sort[0][column]=period&sort[0][direction]=desc&offset=0&length={length}"
        self.all_data: List[Dict] = Browser(endpoint=endpoint).parse_content().get('response').get('data')

    @property
    def get_all_data(self) -> List[Dict]:
        return self.all_data
