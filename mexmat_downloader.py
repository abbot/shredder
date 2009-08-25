#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from urllib2 import urlopen, Request, HTTPError
import os, sys, optparse, random
from HTMLParser import HTMLParser
from urlparse import urljoin
from subprocess import Popen

download_link = None

def find_download_link(tag, attrs):
    global download_link
    if tag.lower() == 'a':
        for a, v in attrs:
            if a.lower() == 'href':
                if 'download' in v:
                    download_link = v

def main():
    global download_link
    p = optparse.OptionParser(usage="%prog url...")
    (options, args) = p.parse_args()
    if len(args) != 1:
        p.print_help()
        sys.exit(1)

    url = args[0]
    random.seed()
    ip = '158.250.33.%d' % random.randint(16, 250)
    user_agent = 'Mozilla/5.0 (X11; U; OpenVMS AlphaServer_ES40; en-US; rv:1.4) Gecko/20030826 SWB/V1.4 (HP)'

    req = Request(url)
    req.add_header('X-Forwarded-For', ip)
    req.add_header('User-Agent', user_agent)
    fd = urlopen(req)
    page = fd.read()
    fd.close()

    p = HTMLParser()
    p.handle_starttag = find_download_link
    p.feed(page)
    if not download_link:
        print "Download link not found on %s." % url
        sys.exit(100)

    full_link = urljoin(url, download_link)
    print "============================================================"
    print "* Download link: %s" % full_link
    print "============================================================"
    print

    wget = Popen(['wget',
                  '--header', 'X-Forwarded-For: %s' % ip,
                  '--referer', url,
                  '-U', user_agent,
                  '--content-disposition',
                  full_link])
    os.waitpid(wget.pid, 0)
    sys.exit(0)

if __name__ == '__main__':
    main()
