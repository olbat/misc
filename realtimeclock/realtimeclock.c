#include "realtimeclock.h"
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <asm/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luc Sarzyniec <olbat@xiato.com>");
MODULE_DESCRIPTION("real time clock module");

module_init(rtc_init);
module_exit(rtc_cleanup);

#define DEVICE_NAME "realtimeclock"
/* sec, min, hour, day, month, year */
#define TIME_BUFFER_SIZE 6

static int device_major;
static int device_status;
static struct file_operations fops = {
	.read = device_read,
	.write = device_write,
	.open = device_open,
	.release = device_release
};
static struct proc_dir_entry *proc_file;
static __u8 time[TIME_BUFFER_SIZE];
static __u8 *time_ptr;


#define RTC_UPDATE(t) \
	t[0] = CMOS_READ(RTC_SECONDS); \
	t[1] = CMOS_READ(RTC_MINUTES); \
	t[2] = CMOS_READ(RTC_HOURS); \
	t[3] = CMOS_READ(RTC_DAY_OF_MONTH); \
	t[4] = CMOS_READ(RTC_MONTH); \
	t[5] = CMOS_READ(RTC_YEAR);

static int __init rtc_init(void)
{
	device_major = register_chrdev(0,DEVICE_NAME,&fops);

	if (unlikely(device_major < 0)) {
		printk(KERN_ALERT "failed register %s errno %d\n",
		       DEVICE_NAME,device_major);	
		return device_major;
	}

	proc_file = create_proc_entry(DEVICE_NAME, 0644, NULL);
	
	if (unlikely(proc_file == NULL)) {
		remove_proc_entry(DEVICE_NAME,&proc_root);
		printk(KERN_ALERT "failed create /proc/%s\n",DEVICE_NAME);
		return -ENOMEM;
	}

	printk(KERN_INFO "%s registered and ready to use\n"
	       "major device number : %d\n"
	       "use 'mknod /dev/%s c %d 0' to create a device file\n"
	       "device output format : ssmmhhDDMMYY\n"
	       "you can use /proc/%s to get informations\n",
	       DEVICE_NAME,device_major,DEVICE_NAME,device_major,DEVICE_NAME);
	device_status = 0;

	proc_file->read_proc 	= procfile_read;
	proc_file->owner 	= THIS_MODULE;
	proc_file->mode		= S_IFREG | S_IRUGO;
	proc_file->uid		= 0;
	proc_file->gid		= 0;
	proc_file->size		= 0;

	return 0;
}

static void __exit rtc_cleanup(void)
{
	int ret = unregister_chrdev(device_major,DEVICE_NAME);

	if (unlikely(ret < 0))
		printk(KERN_ALERT "failed unregister %s, errno %d\n",
		       DEVICE_NAME,ret);
	else
		printk(KERN_INFO "%s unregistred\n"
		       "don't forget to remove the device file if there is one\n",
		       DEVICE_NAME);
	
	remove_proc_entry(DEVICE_NAME,&proc_root);
}

static int device_open(struct inode *inode, struct file *file)
{
	if (unlikely(device_status)) {
		return -EBUSY;
	}

	device_status++;
	
	RTC_UPDATE(time)
	
	time_ptr = time;
	try_module_get(THIS_MODULE);

	return 0;
}

static int device_release(struct inode *inode, struct file *file)
{
	device_status--;
	module_put(THIS_MODULE);
	return 0;
}

static ssize_t
device_read(struct file *file, char *buff, size_t len, loff_t *offset)
{
	ssize_t bytes_read = 0;
	
	while (len && (time_ptr < (time + TIME_BUFFER_SIZE))) {
		put_user(*(time_ptr++),buff++);
		len--;
		bytes_read++;
	}
	return bytes_read;
}

static ssize_t
device_write(struct file *file,const char *buff, size_t len, loff_t *offset)
{
	printk(KERN_ALERT "You can't write in that device.\n");
	return -EINVAL;
}

static int 
procfile_read(char *buff, char **buff_location, 
	      off_t offset, int buff_len, int *eof, void *data)
{
	int ret;

	if (offset > 0) {
		return 0;
	}

	RTC_UPDATE(time);
	ret = sprintf(buff,"%.2d:%.2d:%.2d %.2d/%.2d/%.2d\n",
		      time[2],time[1],time[0],time[3],time[4],time[5]);
	return ret;
}

