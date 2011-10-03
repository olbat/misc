#!/bin/bash -e

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

function __shlog_usage {
	echo "usage: shlog <command> [<param>]"
	echo "commands:"
	echo -e "\t- start\t\t\t: start a new recording session"
	echo -e "\t- edit <filename>\t: edit a file and record the diff"
	echo -e "\t- comment\t\t: add a comment"
	echo -e "\t- stop\t\t\t: stop a recording session and get the log"
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
		__shlog_usage
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
			echo -e "user\t: ${USER}\nhost\t: ${HOSTNAME}" \
				"\ndate\t: `date +'%x %R'`\ncurpath\t: ${PWD}" \
				> $(__shlog_path)/session
			cp $HISTFILE $(__shlog_path)/`basename $HISTFILE`
		fi
		;;
	stop)
		if [ -e "$(__shlog_path)/session" ]
		then

		history -w 

		echo -e "== Session ==\n`cat $(__shlog_path)/session`\n"
		echo "== Commands =="
		local editfiles=0
		local editlog=""

		while read line
		do
			if [ -n "`echo $line | grep "^$FUNCNAME"`" ]
			then

			case `echo $line | cut -d' ' -f2` in
			edit)

				let editfiles=editfiles+1

				local tmp=`cat $(__shlog_path)/files \
					| sed -n "${editfiles}p"`
				local tmpfilebase=`echo $tmp | cut -d " " -f1`
				local realfile=`echo $tmp | cut -d " " -f2`

				echo ">>> Edit $realfile, see [$editfiles]"
				editlog="${editlog}\n[$editfiles] Edit $realfile"
				editlog="${editlog}\n$(cd $tmpfilebase && \
					diff -U1 -NB old new)\n"
				
				;;
			comment)
				echo ">>> ${line#* * }"
				;;
			*)
				echo $line
				;;
			esac

			else
				if [ "$USER" == "root" ]
				then
					local sufchr="#"
				else
					local sufchr="$"
				fi

				echo ${USER}@${HOSTNAME}$sufchr $line
			fi
		done < <(diff -BN $(__shlog_path)/`basename $HISTFILE` $HISTFILE \
		| grep '^>.*$' | sed -e 's/^> //' -e '$d')
		if [ -n "$editlog" ]
		then
			echo -n -e "\n== Files ==${editlog}"
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
	comment)
		echo "comment added"
		;;
	help)
		__shlog_usage
		;;
	*)
		echo "unknown command '$1'"
		;;
	esac

fi

}
########
