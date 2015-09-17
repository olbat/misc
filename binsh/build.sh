#!/bin/bash -e

CC=gcc
CFLAGS="-Wall -std=c99 -pedantic -O3 -fomit-frame-pointer -Wno-overlength-strings"

ENCRYPT_SRC=$(pwd)/encrypt.c
BINSH_SRC=$(pwd)/binsh.c
ENCRYPT=$(pwd)/$(basename $ENCRYPT_SRC .c)
BINSH=${3:-$(pwd)/$(basename $BINSH_SRC .c)}

if [ ! -e "${ENCRYPT_SRC}" ]
then
        echo "$ENCRYPT_SRC file is missing"
        exit 1
fi

if [ ! -e "${BINSH_SRC}" ]
then
        echo "$BINSH_SRC file is missing"
        exit 1
fi

if [ $# -lt 1 ]
then
        echo "usage: $0 <script> [<key>|- <output>]"
        exit 1
fi

${CC} ${CFLAGS} -o $ENCRYPT $ENCRYPT_SRC
chmod +x $ENCRYPT

if [ -t 0 ]
then
	if [ $# -lt 2 ]
	then
	        echo "usage: $0 <script> [<key>|- <output>]"
	        exit 1
	else
		SCRIPT='"'$($ENCRYPT $1 $2)'"'
	fi
else
	SCRIPT='"'$(cat | $ENCRYPT $1 $2)'"'
fi

${CC} ${CFLAGS} -o $BINSH $BINSH_SRC -DSCRIPT=$SCRIPT
chmod +x $BINSH

echo "Build of '$(basename $BINSH)' successful"
