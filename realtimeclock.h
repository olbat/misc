#ifndef _REALTIMECLOCK_H
#define _REALTIMECLOCK_H

#include <linux/types.h>
#include <linux/io.h>
#include <linux/fs.h>
#include <linux/proc_fs.h>

#define CMOS_BASE_PORT		0x70
#define RTC_SECONDS		0
#define RTC_MINUTES		2
#define RTC_HOURS		4
#define RTC_DAY_OF_MONTH	7
#define RTC_MONTH		8
#define RTC_YEAR		9

#define RTC_PORT(x) (CMOS_BASE_PORT + (x))
#define CMOS_READ(addr) rtc_cmos_read(addr)

static inline __u8 rtc_cmos_read(__u8 addr)
{
	outb_p(addr,RTC_PORT(0));
	return (__u8) inb_p(RTC_PORT(1));
}

static int rtc_init(void);
static void rtc_cleanup(void);
static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char *, size_t, loff_t *);
static int procfile_read(char *,char **, off_t, int, int *, void *);

#endif
