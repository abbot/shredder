#!/usr/bin/python
# -*- encoding: utf-8 -*-

import datetime
import gpod
import sys
import re
import itertools

db = gpod.Database(sys.argv[1])

need_check = []

for track in itertools.chain(db.Podcasts, db.Master):
    if track['album'] is None:
        continue
    artist = track['artist'].decode('utf-8')
    if u"Эхо Москвы" in artist:
        title = track['title'].decode('utf-8')
        g = re.match(r"^(\d\d).(\d\d).(\d\d\d\d) (\d\d:\d\d)$", title)
        if g is None:
            continue

        parts = g.groups()
        newtitle = "%s.%s.%s %s" % (parts[2], parts[1], parts[0], parts[3])
    
        print "%s: %s -> %s" % (artist, title, newtitle)
        track['title'] = newtitle.encode('utf-8')
    elif u"echo.msk.ru" == track['album'].decode('utf-8'):
        d = datetime.datetime.strptime(track['title'], "%b %d, %H:%M")
        newname = "2011.%02d.%02d %s" % (d.month, d.day, track['artist'])
        print "%s: %s -> %s" % (track['artist'], track['title'], newname)
        track['album'] = "echo.msk.ru - %s" % track['artist']
        track['title'] = newname

db.close()
