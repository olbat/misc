#!/bin/bash -e
#
####
# shlog is a bash script that allow you to record a shell session by logging
# command history and giving diff of edited files
####
# User notes:
# - Install:
# 	Load the script using 'source shlog.bash' (add it to your .bashrc
# 	to load it automatically)
# - Usage:
# 	Start a new record with 'shlog start', log file editing 
# 	with 'shlog edit <filename>', stop the recording and get the logs
# 	with 'shlog stop'
####
# shlog is Copyright (C) 2011 Luc Sarzyniec <mail@olbat.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
####


function __shlog_path {
	echo ${TMPDIR}/shlog/$$
}

function __realpath {
	if [[ $# -gt 0 && "${1:0:1}" != "/" ]]
	then
		local ret=`pwd`/$1
	else
		local ret=$1
	fi
	echo `cd $(dirname $ret) && pwd`/`basename $ret`
}

function shlog {
	if [ $# -lt 1 ]
	then
		echo "usage: $0 <command> [args]"
	else

	case $1 in
	start)
		if [ -e "$(__shlog_path)/session" ]
		then
			echo "Already existing session, use 'stop' before starting a new one"
		else
			if [ ! -e $(__shlog_path) ]
			then
				mkdir -p $(__shlog_path)
			fi

			history -w
			echo "user=${USER}, host=${HOSTNAME}, curpath=${PWD}"\
				> $(__shlog_path)/session
			cp $HISTFILE $(__shlog_path)/`basename $HISTFILE`
		fi
		;;
	stop)
		if [ -e "$(__shlog_path)/session" ]
		then

		history -w 

		echo -e "Session: `cat $(__shlog_path)/session`\n"
		echo "==COMMAND LOG=="
		local tmpfiles=0
		local editlog=""

		while read line
		do
			if [ -n "`echo $line | grep "$FUNCNAME edit"`" ]
			then
				let tmpfiles=tmpfiles+1

				local tmp=`cat $(__shlog_path)/files \
					| sed -n "${tmpfiles}p"`
				local tmpfilebase=`echo $tmp | cut -d " " -f1`
				local realfile=`echo $tmp | cut -d " " -f2`

				echo ">>> Edited $realfile, see [$tmpfiles]"
				editlog="${editlog}\n[$tmpfiles] Edit $realfile"
				editlog="${editlog}\n$(cd $tmpfilebase && \
					diff -U1 -NB old new)\n"
			else
				if [ "$USER" == "root" ]
				then
					local sufchr="#"
				else
					local sufchr="$"
				fi

				echo ${USER}@${HOSTNAME}:.$sufchr $line
			fi
		done < <(diff -BN $(__shlog_path)/`basename $HISTFILE` $HISTFILE \
		| grep '^>.*$' | sed -e 's/^> //' -e '$d')
		if [ -n "$editlog" ]
		then
			echo -n -e "\n==EDIT LOG==${editlog}"
		fi
		echo
		rm -Rf $(__shlog_path)
		
		else
			echo "No current session, use 'start' to create a new one"
		fi
		;;
	edit)
		if [ -e "$(__shlog_path)/session" ]
		then

		if [ $# -lt 2 ]
		then
			echo "filename missing for '$1'"
		else
			local tmpfilebase=`mktemp -d $(__shlog_path)/XXXXXXXX`
			local realpath=$(__realpath $2)

			echo  $tmpfilebase $realpath >> $(__shlog_path)/files

			cp $realpath $tmpfilebase/old &>/dev/null \
			|| touch $tmpfilebase/old

			${EDITOR:-vi} $realpath

			cp $realpath $tmpfilebase/new &>/dev/null \
			|| touch $tmpfilebase/new
		fi
		else
			echo "No current session, use 'start' to create a new one"
		fi
		;;
	help)
		echo "usage: shlog <command> [<param>]"
		echo "commands:"
		echo -e "\t- start\t\t\t: start a new recording session"
		echo -e "\t- edit <filename>\t: edit a file and record the diff"
		echo -e "\t- stop\t\t\t: stop a recording session and get the log"
		;;
	*)
		echo "unknown command '$1'"
		;;
	esac

fi

}

echo 'shlog loaded with success !'
