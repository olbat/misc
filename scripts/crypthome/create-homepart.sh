#!/bin/dash

set -e
set -x

. ${1:-${KADEPLOY_TMP_DIR:-/tmp}/crypthome.env}


# Install cryptsetup if not installed
dpkg -s cryptsetup-bin >/dev/null 2>&1 || (\
	apt-get -qq update && apt-get install -qqy cryptsetup-bin)

# Umount/close the crypted partition (in case of retry)
cat /proc/mounts | grep -q "^${DMAPDEV}[[:space:]]" && umount $DMAPDEV
[ -b $DMAPDEV ] && cryptsetup close $DMAPNAME

# Format the partition using LUKS
cryptsetup luksFormat --batch-mode $HOMEPART $KEYFILE

# Decrypt and mount the partition
cryptsetup luksOpen --key-file=$KEYFILE $HOMEPART $DMAPNAME
mkfs -q -t $FSTYPE $DMAPDEV
sync

# Mount the partition as /home in the system's root install directory
mkdir -p $HOMEDIR
mount -t $FSTYPE $DMAPDEV $HOMEDIR
