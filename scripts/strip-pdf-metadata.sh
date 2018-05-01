#!/bin/bash
set -e
set -x

tmpfile=$(mktemp)
qpdf --linearize --pages "$1" -- --empty "$tmpfile"
mv "$tmpfile" "$1"
