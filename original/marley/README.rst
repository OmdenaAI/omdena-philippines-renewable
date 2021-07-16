Overview
========

This contains various tools for processing rasters.

Install::

    cd marley
    pip install .
    edit config.py

Setup google drive::

    enable google drive api
    create creds
        credentials/create oauth clientid
        select web application
        authorised javascript origins = http://localhost:8080
        authorised redirect urls = http://localhost:8080/ [NOTE THE / on the end]
        download client_secrets.json
        move client_secrets.json to ~/.gdrive.json

ipstartup.py
============

This is optional:
    * imports common packages
    * configures logging
    * configures notebook addins

..warning
    the imported packages are not installed automatically
    install packages you need and comment out the rest

qgis.py
=======

This is not really needed as you can reproject without qgis

If you do use it:

* Qgis is not installed automatically with this package.
* Qgis has to be installed separately - which requires some configuration.
* Easier is to run this from within qgis console.
