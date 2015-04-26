#!/usr/bin/env python
# encoding: utf-8
"""
freegeoip-geolookup.py

Created by Scott Roberts.
Copyright (c) 2015. All rights reserved.

A basic Maltego script to get DNS resource records for an IPv4Address via OpenDNS Investigate.

Requires the MaltegoTransform Python library in your Python Path.
https://github.com/sroberts/MaltegoTransform-Python
"""

import dotenv
import requests
import sys

# from MaltegoTransform import MaltegoEntity
from MaltegoTransform import MaltegoTransform

# Pull in API Key from .env
OPENDNS_TOKEN = dotenv.get_variables(".env")['OPENDNS_TOKEN']


def main():

    # Set up your Transform object. This is the basis for returning results.
    trx = MaltegoTransform()

    # The first item on the commandline is the calling object.
    ipv4address = sys.argv[1]

    try:
        # Make request to OpenDNS Investigate API
        r = requests.get(
            url="https://investigate.api.opendns.com/dnsdb/ip/a/{}.json".format(ipv4address),
            headers={
                "Authorization": "Bearer {}".format(OPENDNS_TOKEN),
            },
        )

        # Assuming 200 valid response
        if r.status_code == 200:

            data = r.json()

            for rr in data["rrs"]:
                trx.addEntity("maltego.DNSName", rr['rr'][:-1])

            trx.returnOutput()

        else:
            # In the event we can't reach the API end point we want to return an error.
            if r.status_code == 404:
                trx.addException("404: Couldn't reach OpenDNS Investigate.")
            elif r.status_code == 403:
                trx.addException("403: Lookup limit exceeded.")
            else:
                trx.addException("Unknown Error.")

            # ThrowExceptions returns the errored transform.
            trx.throwExceptions()

    except requests.exceptions.RequestException:  # as e:
        print('HTTP Request failed')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "User aborted."
    except SystemExit:
        pass
