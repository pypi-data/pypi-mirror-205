#!/usr/bin/env python3
from typing import List, Dict

API_KEY: str = "Z58UNXyRhL0iDpZUtj6aZPhN9y2nHH7OHPBRXT5i"
STATE: List[str] = ["California", "Colorado", "Florida", "Massachusetts", "Minnesota", "New York", "Ohio", "Texas", "Washington"]
REGION: Dict = {'New York': 'East Coast',
                 'Massachusetts': 'East Coast',
                 'Ohio': 'Midwest',
                 'Minnesota': 'Midwest',
                 'Texas': 'Gulf Coast',
                 'Florida': 'Gulf Coast',
                 'Colorado': 'Rocky Mountain',
                 'California': 'West Coast',
                 'Washington': 'West Coast'}

REGION_REVERSE: Dict = {'East Coast': 'Massachusetts',
                        'MidWest': 'Minnesota',
                        'Gulf Coast': 'Florida',
                        'Rocky Mountain': 'Colorado',
                        'West Coast': 'Washington'}

MOVEMENT_FACETS: Dict = {'Gulf Coast': 'MTTNRP31',
                         'West Coast': 'MTTNRP51',
                         'East Coast': 'MTTNRP11',
                         'Rocky Mountain': 'MTTNRP41',
                         'Midwest' : 'MTTNRP21'}





