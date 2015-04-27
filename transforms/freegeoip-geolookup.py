#!/usr/bin/env python
# encoding: utf-8
"""
freegeoip-geolookup.py

Created by Scott Roberts.
Copyright (c) 2015. All rights reserved.

A basic Maltego script to geolocate IPv4Addresses using Freegeoip.net.

Requires the MaltegoTransform Python library in your Python Path.
https://github.com/sroberts/MaltegoTransform-Python

TODO Has no error handling in the event of a failed lookup or rate limiting.
"""

import requests
import sys

# from MaltegoTransform import MaltegoEntity
from .MaltegoTransform import MaltegoTransform

__version__ == '0.0.1'

class GeoLookup(object):

    """Adds enhanced geolookups for Maltego"""

    def __init__(self, maltegofy=False):
        self.maltegofy = maltegofy

    def freegeoip(self, ipv4address):
        """Looks up ipv4address based on freegeoip.net"""

        # Now we do some Requests Magic :tm: to geolocate the IP.
        r = requests.get('https://freegeoip.net/json/{}'.format(ipv4address))

        # Set up your Transform object. This is the basis for returning results.

        # Parse out the data as JSON.
        data = r.json()
        strings = [data['city'], data['region_name'], data['country_name']]

        self._output(strings)


    def _output(self, values):

        if self.maltegofy:
            trx = MaltegoTransform()

            for value in values:
                trx.addEntity("maltego.Location", value)

            trx.returnOutput()
        else:
            sys.stdout.write('\", \"'.join(filter(None, values)))

def main():
    """Because commandline is always an option."""

    parser = ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-f', '--freegeoip', dest='freegeoip', default=None,
                        help='[OPTIONAL] An IoC to attribute.')
    parser.add_argument('--maltego', dest='maltego', default=False, action='store_true',
                        help='[OPTIONAL] Run in Maltego compatibility mode.')
    args, _ = parser.parse_known_args()

    tb = ThreatButt(args.maltego)

    if args.ioc:
        tb.clown_strike_ioc(args.ioc)

    elif args.md5:
        tb.bespoke_md5(args.md5)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()



# # In the event we can't reach the API end point we want to return an error.
# if r.status_code == 404:
#     trx.addException("404: Couldn't reach FreeGeoIP.net.")
# elif r.status_code == 403:
#     trx.addException("404: Lookup limit exceeded.")
# else:
#     trx.addException("Unknown Error.")
#
# # ThrowExceptions returns the errored transform.
# trx.throwExceptions()
