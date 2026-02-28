# realtimeclock

## About
GNU/Linux kernel module that reads the current time directly from the CMOS real-time clock hardware (port 0x70).

Exposes the time via a character device and procfs interface.

## Usage
```
$ make
$ sudo insmod realtimeclock.ko
$ cat /proc/realtimeclock
```
