import os
import sys
import importlib
import atexit
from os.path import dirname, join
import glob
try:
    from falconpy import oauth2 as FalconAuth
except ImportError as no_falconpy:
    try:
        from . import oauth2 as FalconAuth
    except ImportError as no_falconpy:
        raise SystemExit(
            "The CrowdStrike SDK must be installed in order to use this utility.\n"
            "Install this application with the command `python3 -m pip install crowdstrike-falconpy`."
        ) from no_falconpy


def help(item=None):  # pylint: disable=W0622
    """Debugger help function. Overrides the built in python function."""
    text = """
    This is an interactive Python shell. Python help is available under python_help().

    AUTHENTICATION
    If you have FALCON_CLIENT_ID and FALCON_CLIENT_SECRET environment variables set,
    this shell will authenticate you at start up. You can also call the init()
    function passing the values dbg_falcon_client_id and dbg_falcon_client_secret, or
    you can pass a credential dictionary containing them.

    Additionally if you have FALCON_BASE_URL environmental set, you can connect to
    other environments such as us-gov-1, or us-gov-2.

    AVAILABLE VARIABLES
        'DEBUG_TOKEN' - your OAuth2 token.
        'AUTH_OBJECT' - an instance of the OAuth2 authorization class (authenticated).

    LISTING AVAILABLE SERVICE CLASSES
    Use list_modules() to retrieve a list of all available service classes.

    IMPORTING MODULES
    Use import_module("MODULE_NAME") to import any of the available service classes.

    Import hosts module and query for a specific host:
    In [1]: hosts = import_module("hosts")
    In [2]: hosts.QueryDevicesByFilter(filter="hostname:'whatever'")

    Importing the detects module and querying for all available detections with one command:
    In [1]: import_module("detects").QueryDetects()

    EXIT THE DEBUGGER
    Use exit() to exit the debugger.
    """
    if item is None:
        print(text)
    elif callable(getattr(item, 'help', None)):
        item.help()
    else:
        print(item.__doc__)


def embed():
    """Embed the IPython interactive shell."""
    # _ = importlib.import_module("IPython.terminal.embed")
    # ipshell = _.InteractiveShellEmbed(banner1=BANNER)
    # ipshell.confirm_exit = False
    # ipshell()
    print(BANNER)
    import code; code.interact(local=dict(globals(), **locals()))


def list_modules():
    """List all available Service Classes."""
    modules = glob.glob(join(dirname(__file__), "*.py"))
    result = []
    for key in modules:
        branched = key.split("/")
        position = len(branched)-1
        module_name = branched[position].replace(".py", "")
        if "_" not in module_name[0] and module_name not in ["debug", "api_complete"]:
            result.append(module_name)
    result.sort()
    print("Available modules")
    msg = ""
    for idx, val in enumerate(result):
        msg = f"{msg}%-35s" % val
        cnt = idx + 1
        if cnt % 2 == 0:
            print(msg)
            msg = ""
    print(msg)
    print("\nLoad modules with import_module('MODULE_NAME')")


def import_module(module: str = None):
    """Dynamically imports the module requested and returns an authenticated instance of the Service Class."""
    returned_object = False
    found = False
    if module:
        module = module.lower()
        import_location = "src.falconpy"
        try:
            # Assume they're working from the repo first
            _ = [importlib.import_module(f"{import_location}.{module}")]
            found = True
        except ImportError:
            try:
                import_location = "falconpy"
                # Then try to import from the installed module
                _ = [importlib.import_module(f"{import_location}.{module}")]
                found = True
            except ImportError:
                print("Unable to import requested service class")
        if found:
            current_module = sys.modules[f"{import_location}.{module}"]
            for key in dir(current_module):
                if isinstance(getattr(current_module, key), type) and not key == "ServiceClass" and "_" not in key:
                    _.append(getattr(_[0], key))
                    returned_object = _[1](auth_object=AUTH_OBJECT)
                    print(f"Service Class {key} imported successfully.")
    else:
        print("No module specified.")

    return returned_object


def exit_handler():
    """Revoke the DEBUG_TOKEN and gracefully quit the debugger. Overrides the built in python function."""
    if AUTH_OBJECT:
        print("Discarding token")
        AUTH_OBJECT.revoke(token=DEBUG_TOKEN)
    sys.exit(0)


def startup(dbg_falcon_client_id: str, dbg_falcon_client_secret: str, dbg_falcon_base_url: str):
    """Authenticate using the credentials provided and return the token / authentication object."""
    auth_object = FalconAuth.OAuth2(creds={
        'client_id': dbg_falcon_client_id,
        'client_secret': dbg_falcon_client_secret},
        base_url=dbg_falcon_base_url
    )

    try:
        debug_token = auth_object.token()["body"]["access_token"]
    except KeyError:
        debug_token = False
        auth_object = False

    return debug_token, auth_object


def init(dbg_falcon_client_id: str = None, dbg_falcon_client_secret: str = None, dbg_falcon_base_url: str = "auto", creds: dict = None):
    """Initialize the debugger by retrieving any available credentials and performing initial authentication."""
    if creds:
        dbg_falcon_client_id = creds["falcon_client_id"]
        dbg_falcon_client_secret = creds["falcon_client_secret"]
        dbg_falcon_base_url = creds["falcon_base_url"]

    if "FALCON_CLIENT_ID" in os.environ and "FALCON_CLIENT_SECRET" in os.environ:
        dbg_falcon_client_id = os.environ["FALCON_CLIENT_ID"]
        dbg_falcon_client_secret = os.environ["FALCON_CLIENT_SECRET"]

    if "FALCON_BASE_URL" in os.environ:
        dbg_falcon_base_url = os.environ["FALCON_BASE_URL"]

    global DEBUG_TOKEN, AUTH_OBJECT  # pylint: disable=W0603
    DEBUG_TOKEN, AUTH_OBJECT = startup(dbg_falcon_client_id, dbg_falcon_client_secret, dbg_falcon_base_url)
    embed()


# Move the internal python help() function to python_help()
python_help = help

# Configure our banner
BANNER = """
,---.     |                   ,--.      |
|__. ,---.|    ,---.,---.,---.|   |,---.|---..   .,---.
|    ,---||    |    |   ||   ||   ||---'|   ||   ||   |
`    `---^`---'`---'`---'`   '`--' `---'`---'`---'`---|
                                                  `---'
     CrowdStrike Python 3 Console Debug (not iPython)
          * Customized for BaseURL access * 

This shell-like interface allows for quick learning,
demoing, and prototyping of API operations using
the CrowdStrike FalconPy SDK and Python 3.

Please type help() to learn more.
                         |
     _____________   __ -+- _____________
     \\_____     /   /_ \\ |   \\     _____/
       \\_____   \\____/  \\____/    _____/
         \\_____    FalconPy      _____/
           \\___________  ___________/
                     /____\\
"""

# Default our debug token and auth object to False
DEBUG_TOKEN = False
AUTH_OBJECT = False

atexit.register(exit_handler)

init()
