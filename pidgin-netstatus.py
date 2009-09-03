#!/usr/bin/env python

import dbus, optparse, sys

def pidgin_getiface():
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
    return purple
    
def pidgin_disconnect():
    p = pidgin_getiface()
    #s = p.PurpleSavedstatusNew("Offline", 1)
    #p.PurpleSavedstatusActivate(s)
    conns = p.PurpleConnectionsGetAll()
    for conn in conns:
        p.PurpleConnectionDestroy(conn)

def pidgin_connect():
    p = pidgin_getiface()
    accts = p.PurpleAccountsGetAll()
    for acct in accts:
        p.PurpleAccountConnect(acct)

def main():
    p = optparse.OptionParser()
    p.add_option("-c", "--connect", action="store_true")
    p.add_option("-d", "--disconnect", action="store_true")
    opts, args = p.parse_args()

    if opts.connect:
        pidgin_connect()
    elif opts.disconnect:
        pidgin_disconnect()
    else:
        p.print_help()
        sys.exit(1)

    sys.exit(0)

if __name__=='__main__':
    main()
