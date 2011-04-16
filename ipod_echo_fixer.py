#!/usr/bin/python
# -*- encoding: utf-8 -*-

import gpod
import sys
import re

db = gpod.Database(sys.argv[1])

need_check = []

for track in db.Podcasts:
    artist = track['artist'].decode('utf-8')
    if u"Эхо Москвы" not in artist:
        continue

    title = track['title'].decode('utf-8')
    g = re.match(r"^(\d\d).(\d\d).(\d\d\d\d) (\d\d:\d\d)$", title)
    if g is None:
        continue

    parts = g.groups()
    newtitle = "%s.%s.%s %s" % (parts[2], parts[1], parts[0], parts[3])
    
    print "%s: %s -> %s" % (artist, title, newtitle)
    track['title'] = newtitle.encode('utf-8')

db.close()
