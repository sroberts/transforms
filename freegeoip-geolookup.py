#!/usr/bin/env python
# encoding: utf-8
"""
freegeoip-geolookup.py

Created by Scott Roberts.
Copyright (c) 2015. All rights reserved.

A basic Maltego script to geolocate IPv4Addresses using Freegeoip.net.

Requires the MaltegoTransform Python library in your Python Path.
https://github.com/sroberts/MaltegoTransform-Python
"""

import requests
import sys

# from MaltegoTransform import MaltegoEntity
from MaltegoTransform import MaltegoTransform

def main():

    # Set up your Transform object. This is the basis for returning results.
    trx = MaltegoTransform()

    # The first item on the commandline is the calling object.
    ipv4address = sys.argv[1]

    # Now we do some Requests Magic :tm: to geolocate the IP.
    r = requests.get('https://freegeoip.net/json/{}'.format(ipv4address))

    # Double check we got back a valid result.
    if r.status_code == 200:

        # Parse out the data as JSON.
        data = r.json()
        strings = [data['city'], data['region_name'], data['country_name']]

        # This is a 1-1 transform, so we create one location entity based
        # on the geolocation data.
        trx.addEntity("maltego.Location", ', '.join(filter(None, strings)))

        # This returns the transform as an XML representation that Maltego
        # uses to update the graph.
        trx.returnOutput()

    else:
        # In the event we can't reach the API end point we want to return an error.
        if r.status_code == 404:
            trx.addException("404: Couldn't reach FreeGeoIP.net.")
        elif r.status_code == 403:
            trx.addException("404: Lookup limit exceeded.")
        else:
            trx.addException("Unknown Error.")

        # ThrowExceptions returns the errored transform.
        trx.throwExceptions()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "User aborted."
    except SystemExit:
        pass