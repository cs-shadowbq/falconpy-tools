# flake8: noqa=W605  pylint: disable=W1401
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
try:
    from falconpy import APIHarness
except ImportError as no_falconpy:
    raise SystemExit(
        "The CrowdStrike SDK must be installed in order to use this utility.\n"
        "Install this application with the command `python3 -m pip install crowdstrike-falconpy`."
    ) from no_falconpy

parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawTextHelpFormatter
)
parser.add_argument('-k', '--key', help="CrowdStrike API Key", required=True)
parser.add_argument('-s', '--secret', help="CrowdStrike API Secret", required=True)
parser.add_argument('-x', '--skip-ssl', help="Skip SSL verification", required=False, action='store_true')
parser.add_argument('-b', '--base_url', help="CrowdStrike base URL for Gov Clouds", required=False, default="auto")

# add verbose options
parser.add_argument('-v', '--verbose', help="Enable verbose mode", required=False, action='store_true')

args = parser.parse_args()
CLIENT_ID = args.key
CLIENT_SECRET = args.secret
CLIENT_BASE = args.base_url

# Login to the Falcon API and retrieve our list of sensors
if args.base_url == "auto":
    if args.skip_ssl:
        falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, ssl_verify=False)
    else:
        falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
else:
    if args.skip_ssl:
        falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, base_url=CLIENT_BASE, ssl_verify=False)
    else:
        falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, base_url=CLIENT_BASE)

if falcon.authenticate():
    if args.verbose:
        print("Authentication successful")
    sys.exit(0)
else:
    if args.verbose:
        print("Authentication failed")
    sys.exit(1)
