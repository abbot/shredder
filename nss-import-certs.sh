#!/bin/sh

for certfile in /etc/grid-security/certificates/*.0 ; do
  dn=`openssl x509 -in $certfile -subject -noout | cut -c 10-`
  certutil -A -n "Grid CA: $dn" -t CT,C,C -d . -i $certfile
  echo imported $dn
done
