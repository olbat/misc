#!/bin/bash

# This script only tests the notAfter field of the x509 certificates

set -e

function test_cert_date {
	local crt="$(openssl s_client -connect 2>/dev/null $1 </dev/null)"
	[ -n "$crt" ] && openssl x509 -noout -enddate <<< "$crt" | cut -d= -f2 \
	| [ $(/bin/date -u +%s -f-) -gt $(/bin/date -u +%s) ]
}

[ $# -eq 0 ] && (echo "usage: $0 [<host1:port1> <host2:port2> ...|-]" ; exit 1)
[ "$1" == "-" ] && list=$(</dev/stdin) || list="$@"

exit_status=0

for hostport in $list
do
	if test_cert_date "$hostport"
	then
		echo "${hostport} OK"
	else
		echo "!${hostport} KO"
		exit_status=1
	fi
done

exit $exit_status
