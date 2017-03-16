#!/bin/bash

set -e
set -x

. ${1:-${KADEPLOY_TMP_DIR:-/tmp}/crypthome.env}

# Install cryptsetup in ROOTDIR if not installed
chroot $ROOTDIR /usr/bin/dpkg -s cryptsetup-bin >/dev/null 2>&1 \
	|| (chroot $ROOTDIR /usr/bin/apt-get -qq update \
	   && chroot $ROOTDIR /usr/bin/apt-get install -qqy cryptsetup-bin)

# Update /etc/fstab and /etc/crypttab entries
mkdir -p ${ROOTDIR}/etc
uuid=$(blkid -p -u filesystem -s UUID -o value $DMAPDEV)

[ -e ${ROOTDIR}/etc/fstab ] && sed -i ${ROOTDIR}/etc/fstab \
	-e "/^${DMAPDEV//\//\\/}[[:space:]]/d" \
	-e "/^${HOMEPART//\//\\/}[[:space:]]/d" \
	-e "/^[^[:space:]]\+[[:space:]]\+\/home[[:space:]]/d"
echo -e "${DMAPDEV}\t/home\t${FSTYPE}\tdefaults,noauto\t0\t2"\
	>> ${ROOTDIR}/etc/fstab

[ -e ${ROOTDIR}/etc/crypttab ] \
	&& sed -e "/^[^[:space:]]\+[[:space:]]\+UUID=${uuid}[[:space:]]/d" \
		-i ${ROOTDIR}/etc/crypttab
echo "${DMAPNAME} UUID=${uuid} none luks,noauto" >> ${ROOTDIR}/etc/crypttab

# Add warning in /etc/profile
mkdir -p ${ROOTDIR}/etc/profile.d
cat << EOF > ${ROOTDIR}/etc/profile.d/crypthome-warning.sh
if ! grep -q "^${DMAPDEV}[[:space:]]" /proc/mounts; then
  echo -e "\nWarning: the encrypted /home partition is not mounted !"\
    "\n\nPlease decrypt and mount it using:\n"\
    "# cryptsetup luksOpen --key-file=KEYFILE ${HOMEPART} ${DMAPNAME}\n"\
    "# mount /home\n" 1>&2
fi
EOF

# Copy the home directory of the root user to the home partition
roothomedir=$(chroot $ROOTDIR /usr/bin/getent passwd root | cut -d':' -f6)
cp -rp ${ROOTDIR}${roothomedir} ${HOMEDIR}/root

# Move the home directory of the root user to /home
umount $HOMEDIR
chroot $ROOTDIR /usr/sbin/usermod --home=/home/root --move-home root
mount $DMAPDEV $HOMEDIR
