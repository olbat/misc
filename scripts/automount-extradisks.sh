#!/bin/bash

set -x
set -e

ROOT_PART=${1:-/dev/sda1}
MOUNTP=${2:-/mnt/data} # will be suffixed by a number
ROOT_DIR=${3:-/}

# List additional disks
num=0
for dev in $(lsblk -S -o type,name -n | grep '^disk' | awk '{print $2}')
do
    [ "/dev/$dev" == $ROOT_PART ] && continue

    # List the partitions
    for part in $(lsblk /dev/$dev -o name -l -n | tail -n+2)
    do
	# Get UUID and TYPE of partitions that contains a filesystem
	uuid=$(blkid -p -u filesystem -s UUID -o value /dev/$part) || continue
	fstype=$(blkid -p -u filesystem -s TYPE -o value /dev/$part)

	# Do not mount encrypted filesystems
	echo $fstype | grep -q '^crypto_' && continue

	# Create the mountpoint directory
	mkdir -p ${ROOT_DIR}${MOUNTP}${num}

	# Remove existing entries from /etc/fstab
	sed -i -e "/^UUID=${uuid}[[:space:]]/d" ${ROOT_DIR}/etc/fstab

	# Create the entry in /etc/fstab
        echo -e "UUID=${uuid}\t${MOUNTP}${num}\t${fstype}\tdefaults,rw\t0\t2"\
            >> ${ROOT_DIR}/etc/fstab

	# Mount the partition
	mount UUID=$uuid

	let num+=1
    done
done

exit 0
