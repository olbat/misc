#!/bin/bash -e

CC=gcc
CFLAGS="-Wall -std=c99 -pedantic -O3 -fomit-frame-pointer"
SHBIN_SRC=$(pwd)/shbin.c
BINSH_SRC=$(pwd)/binsh.c
SHBIN=$(pwd)/$(basename $SHBIN_SRC .c)
BINSH=${3:-$(pwd)/$(basename $BINSH_SRC .c)}

if [ ! -e "${SHBIN_SRC}" ]
then
        echo "$SHBIN_SRC file is missing"
        exit 1
fi

if [ ! -e "${BINSH_SRC}" ]
then
        echo "$BINSH_SRC file is missing"
        exit 1
fi

if [ $# -lt 2 ]
then
        echo "usage: $0 <script> <key> [<output>]"
        exit 1
fi

${CC} ${CFLAGS} -o $SHBIN $SHBIN_SRC
chmod +x $SHBIN
SCRIPT='"'$($SHBIN $1 $2)'"'
${CC} ${CFLAGS} -o $BINSH $BINSH_SRC -DSCRIPT=$SCRIPT
chmod +x $BINSH

echo "Build of '$(basename $BINSH)' successful"
