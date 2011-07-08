#!/usr/bin/python

from hashlib import md5
import logging
import os
import optparse
import re
import sys

log = logging.getLogger("dups")

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--debug", action="store_true", default=False)
    opts, args = parser.parse_args()

    return opts, args

class SameFile(object):
    def __init__(self, path):
        self.path = path
        self.s = os.stat(path)
        self.md5 = None

    def checksum(self):
        if self.md5 is None:
            log.debug("Calculating md5 for %s", self.path)
            md = md5()
            fd = open(self.path, "rb")
            while True:
                block = fd.read(1024*1024)
                if block == "":
                    break
                md.update(block)
            self.md5 = md.hexdigest()
        return self.md5

    def __hash__(self):
        return hash(self.s.st_size)

    def __cmp__(self, other):
        if not isinstance(other, SameFile):
            raise NotImplementedError()
        if other.s.st_size != self.s.st_size:
            return cmp(self.s.st_size, other.s.st_size)
        else:
            return cmp(self.checksum(), other.checksum())

    def __repr__(self):
        return "SameFile(%s)" % repr(self.path)

def statfiles(d, dirname, filenames):
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if os.path.isfile(path) and not os.path.islink(path):
            d.append(SameFile(path))

def main():
    opts, args = parse_args()

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    d = []
    for place in args:
        os.path.walk(place, statfiles, d)

    dups = {}
    for f in d:
        dups.setdefault(f, [])
        dups[f].append(f)

    for f, v in dups.iteritems():
        if len(v) > 1:
            print "%d: %s" % (len(v),
                              " ".join(f.path.replace(" ", r"\ ") for f in v))

if __name__ == '__main__':
    main()
