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
parser.add_argument('-b', '--base', help="CrowdStrike base URL for Gov Clouds", required=False, default="auto")
args = parser.parse_args()
CLIENTID = args.key
CLIENTSECRET = args.secret
CLIENTBASE = args.base

# Login to the Falcon API and retrieve our list of sensors
if args.base == "auto":
  falcon = APIHarness(client_id=CLIENTID, client_secret=CLIENTSECRET)
else:
  falcon = APIHarness(client_id=CLIENTID, client_secret=CLIENTSECRET, base_url=CLIENTBASE)

if falcon.authenticate():
    sys.exit(0)
else:
    sys.exit(1)
