# falconpy-tools
```
    ___       _                                                     _       
   / __)     | |                                     _             | |      
 _| |__ _____| | ____ ___  ____  ____  _   _ _____ _| |_ ___   ___ | |  ___ 
(_   __|____ | |/ ___) _ \|  _ \|  _ \| | | (_____|_   _) _ \ / _ \| | /___)
  | |  / ___ | ( (__| |_| | | | | |_| | |_| |       | || |_| | |_| | ||___ |
  |_|  \_____|\_)____)___/|_| |_|  __/ \__  |        \__)___/ \___/ \_|___/ 
                                |_|   (____/                                
```
Collection of tools to use with CrowdStrike falonpy SDK

For CrowdStrike Cloud Workload Protection: https://github.com/cs-shadowbq/falcon-cwp-tools

## Requirements

[FalconPy SDK](https://github.com/CrowdStrike/falconpy). These can be installed via pip:

```shell
$ python3 -m pip install crowdstrike-falconpy tabulate
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

### `falcon_download_sensor.py`

```
usage: falcon_download_sensor.py [-h] -k KEY -s SECRET [-b BASE] [-a] [-d] [-c COMMAND] [-o OS] [-v OSVER] [-n FILENAME] [-f FORMAT]

CrowdStrike Falcon Sensor Download utility.

            CrowdStrike Falcon
 _______                               ______                        __                __
|   _   .-----.-----.-----.-----.----.|   _  \ .-----.--.--.--.-----|  .-----.---.-.--|  |
|   1___|  -__|     |__ --|  _  |   _||.  |   \|  _  |  |  |  |     |  |  _  |  _  |  _  |
|____   |_____|__|__|_____|_____|__|  |.  |    |_____|________|__|__|__|_____|___._|_____|
|:  1   |                             |:  1    /
|::.. . |                             |::.. . /                 - jshcodes@CrowdStrike
`-------'                             `------'

This example requires the crowdstrike-falconpy (0.6.2+) and tabulate packages.

Required API Scope - Sensor Download: READ

options:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     CrowdStrike API Key
  -s SECRET, --secret SECRET
                        CrowdStrike API Secret
  -b BASE, --base BASE  CrowdStrike base URL for Gov Clouds
  -a, --all             Show all columns / Download all versions
  -d, --download        Shortcut for '--command download'
  -c COMMAND, --command COMMAND
                        Command to perform. (list or download, defaults to list)
  -o OS, --os OS        Sensor operating system
  -v OSVER, --osver OSVER
                        Sensor operating system version
  -n FILENAME, --filename FILENAME
                        Name to use for downloaded file
  -f FORMAT, --format FORMAT
                        Table format to use for display.
                        (plain, simple, github, grid, fancy_grid, pipe, orgtbl, jira, presto,
                        pretty, psql, rst, mediawiki, moinmoin, youtrack, html, unsafehtml,
                        latext, latex_raw, latex_booktabs, latex_longtable, textile, tsv)


python3 falcon_download_sensor.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -o ubuntu
╒══════════════════════════════════════╤════════╤══════════════╤══════════════════════════╤════════════╕
│ Name                                 │ OS     │ OS Version   │ Release Date             │ Version    │
╞══════════════════════════════════════╪════════╪══════════════╪══════════════════════════╪════════════╡
│ falcon-sensor_6.45.0-14203_amd64.deb │ Debian │ 9/10/11      │ 2022-09-08T22:20:33.067Z │ 6.45.14203 │
├──────────────────────────────────────┼────────┼──────────────┼──────────────────────────┼────────────┤
│ falcon-sensor_6.44.0-14108_amd64.deb │ Debian │ 9/10/11      │ 2022-08-29T22:06:20.427Z │ 6.44.14108 │
├──────────────────────────────────────┼────────┼──────────────┼──────────────────────────┼────────────┤
│ falcon-sensor_6.43.0-14006_amd64.deb │ Debian │ 9/10/11      │ 2022-08-25T22:10:18.638Z │ 6.43.14006 │
├──────────────────────────────────────┼────────┼──────────────┼──────────────────────────┼────────────┤
│ falcon-sensor_6.41.0-13804_amd64.deb │ Debian │ 9/10/11      │ 2022-07-12T22:13:12.153Z │ 6.41.13804 │
├──────────────────────────────────────┼────────┼──────────────┼──────────────────────────┼────────────┤
│ falcon-sensor_6.40.0-13707_amd64.deb │ Debian │ 9/10/11      │ 2022-07-06T22:21:39.092Z │ 6.40.13707 │
├──────────────────────────────────────┼────────┼──────────────┼──────────────────────────┼────────────┤
│ falcon-sensor_6.38.0-13501_amd64.deb │ Debian │ 9/10/11      │ 2022-04-07T23:23:38.709Z │ 6.38.13501 │
├──────────────────────────────────────┼────────┼──────────────┼──────────────────────────┼────────────┤
│ falcon-sensor_6.37.0-13402_amd64.deb │ Debian │ 9/10/11      │ 2022-03-24T22:06:59.917Z │ 6.37.13402 │
╘══════════════════════════════════════╧════════╧══════════════╧══════════════════════════╧════════════╛

python3 falcon_download_sensor.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -o windows -d
Downloading Falcon Sensor for Windows version 6.46.16008
```
