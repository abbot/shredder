#!/bin/bash

function offline()
{
  for user in `ls -1 /var/run/console | grep -v console.lock` ; do
    su $user -c "/home/shamardin/bin/pidgin-netstatus.py -d"
  done
}

function online()
{
  for user in `ls -1 /var/run/console | grep -v console.lock` ; do
    su $user -c "/home/shamardin/bin/pidgin-netstatus.py -c"
  done
}

export LC_ALL=C

if [ "$2" = "down" ]; then
	/sbin/ip route ls | grep -q ^default || {
		offline && logger "pidgin: status to offline" || :
	} && { :; }
fi

if [ "$2" = "up" ]; then
	/sbin/ip -o route show dev "$1" | grep -q '^default' && {
    		online "status online" && logger "pidgin: status to online" || :
	} || { :; }
fi

