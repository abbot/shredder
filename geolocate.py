#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json
from urllib import urlencode
from urllib2 import urlopen
import operator
import optparse
import sys

def main():
    parser = optparse.OptionParser(usage="%prog radius address...",
                                   description="Download caches for the given address and radius in km")
    opts, args = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    params = urlencode({"sensor": "false",
                        "address": ' '.join(args)})
    url = "http://maps.googleapis.com/maps/api/geocode/json?" + params
    results = json.loads(urlopen(url).read())
    if results['status'] != 'OK':
        print "Results are not OK"
        sys.exit(1)

    for result in results['results']:
        location = result['geometry']['location']
        print "** %s" % result['formatted_address']
        print "%.7f" % location['lat'], "%.7f" % location['lng']
        lat = location['lat']
        lng = location['lng']        
        lat_letter = lat > 0 and 'N' or 'S'
        lng_letter = lng > 0 and 'E' or 'W'
        lat_deg = int(lat)
        lat_sec = (lat - lat_deg) * 60.0
        lng_deg = int(lng)
        lng_sec = (lng - lng_deg) * 60.0
        print "%s %d %02.03f, %s %d %02.03f" % (lat_letter, lat, lat_sec,
                                                lng_letter, lng, lng_sec)
        # print "
        
if __name__ == '__main__':
    main()
