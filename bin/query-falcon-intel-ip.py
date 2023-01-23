# flake8: noqa=W605  pylint: disable=W1401

"""

The MIT License

Copyright(c) 2023 CrowdStrike Inc.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files(the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and / or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

"""

from argparse import ArgumentParser, RawTextHelpFormatter
try:
    from falconpy import Intel
except ImportError as no_falconpy:
    raise SystemExit(
        "The CrowdStrike SDK must be installed in order to use this utility.\n"
        "Install this application with the command `python3 -m pip install crowdstrike-falconpy`."
    ) from no_falconpy

import json

"""
https://www.falconpy.io/Service-Collections/Intel.html#queryintelindicatorentities

Maximum number of records to return. (Max: 5000), so remember to paginate results if needed.

- offset (int) - Set the starting row number to return indicators from.
    Defaults to 0.
- limit (int) - Set the number of indicators to return.
    The number must be between 1 and 50000
- sort (str) - Order fields in ascending or descending order.
    Ex: published_date|asc.
- filter (str) - Filter your query by specifying FQL filter parameters.
    Filter parameters include:
    _marker, actors, deleted, domain_types, id, indicator,
    ip_address_types, kill_chains, labels, labels.created_on,
    labels.last_valid_on, labels.name, last_updated, malicious_confidence, malware_families, published_date, reports, targets, threat_types, type, vulnerabilities.
- q (str) - Perform a generic substring search across all fields.
- include_deleted (bool) - If true, include both published and deleted indicators in the response.
"""


parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawTextHelpFormatter
)
parser.add_argument('-k', '--key', help="CrowdStrike API Key", required=True)
parser.add_argument(
    '-s', '--secret', help="CrowdStrike API Secret", required=True)
parser.add_argument(
    '-b', '--base', help="CrowdStrike base URL for Gov Clouds", required=False, default="auto")
parser.add_argument('-r', '--related', help='Flag indicating if related indicators should be returned',
                    required=False, action="store_true")
parser.add_argument('-a', '--all', help='Show all including disabled indicators',
                    required=False, action="store_true")
parser.add_argument('-j', '--json', help='Show as JSON',
                    required=False, action="store_true")
parser.add_argument('-q', '--query', help='Search for IP Intel Indicator "51.116.1.1" or "51.116.*"',
                    required=True)


args = parser.parse_args()
CLIENT_ID = args.key
CLIENT_SECRET = args.secret
CLIENT_BASE = args.base
Q = args.query

SHOW_RELATED = False
if args.related:
    SHOW_RELATED = True

SHOW_ALL = False
if args.all:
    SHOW_ALL = True

SHOW_JSON = False
if args.json:
    SHOW_JSON = True

# Login to the Falcon API and retrieve our list of sensors
if args.base == "auto":
    falcon = Intel(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
else:
    falcon = Intel(client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET, base_url=CLIENT_BASE)

response = falcon.QueryIntelIndicatorEntities(offset=0,
                                              limit=5000,
                                              filter=f"id:*'ip_address_{Q}'",

                                              include_deleted=SHOW_ALL,
                                              include_relations=SHOW_RELATED
                                              )
CNT = len(response["body"]["resources"])
data = response["body"]["resources"]

desired_indicators = []

for intel_ind in data:
    indicator = str(intel_ind['indicator'])
    if indicator.startswith('51.116'):
        desired_indicators.append(intel_ind)

if SHOW_JSON:
    # Serializing json
    json_object = json.dumps(response["body"]["resources"], indent=4)
    print(json_object)

else:
    print("resources returned: ", CNT)
    if CNT > 0:
        for x in range(CNT):
            print(response["body"]["resources"][x]['indicator'])
            print('malware_families: ',
                  response["body"]["resources"][x]['malware_families'])
            print('Actors: ', response["body"]["resources"][x]['actors'])
            print('reports: ', response["body"]["resources"][x]['reports'])
            print('malicious_confidence: ',
                  response["body"]["resources"][x]['malicious_confidence'])
            print('-----')
