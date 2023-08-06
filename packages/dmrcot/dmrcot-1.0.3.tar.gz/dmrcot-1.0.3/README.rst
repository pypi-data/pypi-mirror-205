DMR to Cursor on Target Gateway
*********************************

.. image:: https://raw.githubusercontent.com/snstac/dmrcot/main/docs/atak_screenshot.png?token=GHSAT0AAAAAAB5KT72KYMKM7HC3VWKFNTQAZCIXEJQ
   :alt: Screenshot of DMRCOT in ATAK.

The DMR to Cursor on Target Gateway (DMRCOT) transforms Tait DMR Unit Information into 
Cursor on Target (CoT) for display on `TAK Products <https://tak.gov/>`_ such as ATAK, 
WinTAK & iTAK.

Concept of Operations
=====================
DMRCOT reads Tait DMR subscriber radio positioning information from a DMR NC.

.. image:: https://raw.githubusercontent.com/snstac/dmrcot/main/docs/dmrcot_conop.png?token=GHSAT0AAAAAAB5KT72KJV6UBJNG6KLWKZTYZCIXFQA
   :alt: DMRCOT Concept of Operations (CONOP).
   :target: https://raw.githubusercontent.com/snstac/dmrcot/main/docs/dmrcot_conop.png


Install
=======
DMRCOT functionality is provided via a command-line tool named ``dmrcot``. 
To install ``dmrcot``:

Debian, Ubuntu, Raspbian, Raspberry OS::
    
    $ sudo apt update
    $ wget https://github.com/snstac/pytak/releases/latest/download/python3-pytak_latest_all.deb
    $ sudo apt install -f ./python3-pytak_latest_all.deb
    $ wget https://github.com/snstac/dmrcot/releases/latest/download/python3-dmrcot_latest_all.deb
    $ sudo apt install -f ./python3-dmrcot_latest_all.deb

CentOS, et al::

    $ sudo python3 -m pip install dmrcot

Install from source::
    
    $ git clone https://github.com/snstac/dmrcot.git
    $ cd dmrcot/
    $ python3 -m pip install .


Usage
=====
The ``dmrcot`` program has several command-line arguments::

    $ dmrcot -h
    usage: dmrcot [-h] [-c CONFIG_FILE] [-p PREF_PACKAGE]

    optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG_FILE, --CONFIG_FILE CONFIG_FILE
                            Optional configuration file. Default: config.ini
    -p PREF_PACKAGE, --PREF_PACKAGE PREF_PACKAGE
                            Optional connection preferences package zip file (aka data package).


Running
=======
DMRCOT should be started as a background sevice (daemon). Most modern systems 
use systemd.


Debian, Ubuntu, RaspberryOS, Raspbian
-------------------------------------
1. Copy the following code block to ``/etc/systemd/system/dmrcot.service``::

    [Unit]
    Description=DMRCOT Service
    After=multi-user.target
    [Service]
    ExecStart=dmrcot -c /etc/dmrcot.ini
    Restart=always
    RestartSec=5
    [Install]
    WantedBy=multi-user.target

(You can create ``dmrcot.service`` using Nano: ``$ sudo nano /etc/systemd/system/dmrcot.service``)

2. Create the ``/etc/dmrcot.ini`` file and add an appropriate configuration, see `Configuration <#Configuration>`_ section of the README::
    
    $ sudo nano /etc/dmrcot.ini

3. Enable cotproxy systemd service::
    
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable dmrcot
    $ sudo systemctl start dmrcot

4. You can view logs with: ``$ sudo journalctl -xef``


Configuration 
-------------
Configuration parameters can be specified either via environment variables or in
a INI-stile configuration file.

Parameters:

* **FEED_URL**: (*optional*) DMR NC source URL.
* **COT_URL**: (*optional*) Destination for CoT messages. See `PyTAK <https://github.com/snstac/pytak#configuration-parameters>`_ for options.
* **POLL_INTERVAL**: (*optional*) Period in seconds to poll **FEED_URL**.

There are other configuration parameters available via `PyTAK <https://github.com/snstac/pytak#configuration-parameters>`_.

Configuration parameters are imported in the following priority order:

1. config.ini (if exists) or -c <filename> (if specified).
2. Environment Variables (if set).
3. Defaults.


Troubleshooting
===============
To report bugs, please set the DEBUG=1 environment variable to collect logs::

    $ DEBUG=1 dmrcot
    $ # -OR-
    $ export DEBUG=1
    $ dmrcot


Source
======
The source for DMRCOT can be found on Github: https://github.com/snstac/dmrcot


License
=======
Copyright 2023 Sensors & Signals LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


A PyTAK Project
===============
.. image:: https://raw.githubusercontent.com/snstac/dmrcot/main/docs/pytak_logo-256x264.png?token=GHSAT0AAAAAAB5KT72LUEKHWJ464J3XTTLUZCIXGAA
    :alt: PyTAK Logo
    :target: https://github.com/snstac/pytak
