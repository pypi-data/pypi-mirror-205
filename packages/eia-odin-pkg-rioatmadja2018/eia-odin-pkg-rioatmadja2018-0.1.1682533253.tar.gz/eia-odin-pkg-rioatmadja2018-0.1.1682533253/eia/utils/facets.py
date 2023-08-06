#!/usr/bin/env python3
from eia.utils.browser import  Browser
from eia.utils.constants import STATE
from typing import Dict

def get_facets_gasoline_price() -> Dict:

    all_facets: Dict = {}
    browser: 'Browser' = Browser(endpoint="https://api.eia.gov/v2/petroleum/pri/gnd/facet/series?api_key=CZdQsisRJzwOfqUWV3jiMPNEx3ZbHcuJ2VQus04i")
    for item in browser.parse_content().get('response').get("facets"):
        for state in STATE:
            if "%s All Grades Conventional Retail Gasoline Prices" % (state) in item.get('name'):
                all_facets[state] = item.get('id')

    return all_facets


