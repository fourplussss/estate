#!/usr/local/bin/python3
import sys

import geocoder
g = geocoder.osm('11 Wall Street, New York')
print(g.osm)
