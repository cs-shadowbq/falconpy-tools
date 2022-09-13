# falconpy-tools
Collection of tools to use with falonpy SDK

## Requirements

[FalconPy SDK](https://github.com/CrowdStrike/falconpy). These can be installed via pip:

```shell
$ python3 -m pip install crowdstrike-falconpy
```

### Optional

* [Secrets](https://github.com/shadowbq/matrix.secrets) - Matrix GPG/RSA secrets method of storing the bash credentials.
* [vault](https://www.vaultproject.io/) - Secure, store and tightly control access to tokens, passwords, certificates, encryption keys for protecting secrets and other sensitive data using a UI, CLI, or HTTP API.

```
$ env |grep FALCON_
FALCON_CLIENT_SECRET=GHIjklmnopqrs123
FALCON_CID=DEFghijklmop456
FALCON_CHKSUM=2a
FALCON_BASE_URL=https://api.laggar.gcw.crowdstrike.com
FALCON_CLIENT_ID=abcdecf123
```

## Tools

### `falcon_validate_creds`

Validate `[ENV]` credentials with custom base urls that responds to proper shell returns.

```
$ python3 ./falcon_validate_creds.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL
$ echo $?
0

$ python3 ./falcon_validate_creds.py -k $BAD_CLIENT_ID -s $BAD_CLIENT_SECRET
$ echo $?
1
```

### `falcon_debug.py`

```
$ python3 falcon_debug.py

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
     \_____     /   /_ \ |   \     _____/
       \_____   \____/  \____/    _____/
         \_____    FalconPy      _____/
           \___________  ___________/
                     /____\

Python 3.10.7 (main, Sep 12 2022, 19:40:04) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> DEBUG_TOKEN
'(..snip..)ALSKDJLASKDJLASKJDLKASJDLKASJDLKJASDLKJASLDKJASLKDJASLKDJLASKDJLASKJDLKASJDM'
```
