#!/bin/bash

set -e

[ $# -lt 1 ] && (echo "usage: $0 <dir>"; exit 1)
[ ! -d $1 ] && (echo "$1 is not a directory"; exit 1)

IFS=$(echo -en "\n\b")

dir=${1%/}
out="../${dir}.cbc"

pushd "${dir}"
rm -f comics.txt
find . -maxdepth 1 -type d -print0 | while read -d $'\0' f
do
	if [ -d "$f" -a "$f" != "." ]
	then
		d=${f%/}

		pushd "${d}"
		echo "- zip ${d}.cbz"
		zip -r "../${d}.cbz" .
		popd

		echo "- zip ${dir}.cbc"
		zip "$out" "${d}.cbz"
		echo "$(basename $d).cbz:$(basename $d)" >> comics.txt
	fi
done
echo "- comics.txt"
sort -n -o comics.txt comics.txt
zip "$out" comics.txt
popd
