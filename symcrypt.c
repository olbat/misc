/*
 * Copyright (C) 2006, 2007 Sarzyniec Luc <olbat@xiato.net>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * see the COPYING file for more informations */

#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <signal.h>
#include <malloc.h>
#include <stdio.h>

/* The software use a unique binary key to crypt files, it is better to use a 
 * long key -more than 512 bytes. 
 * You can use the printfile program on /dev/random to generate one -you can 
 * download it at http://xiato.net/svn/dev/misc/
 */

#define KEY_SOFT __extension__ \
"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12"\
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13"\
"\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14"\
"\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15"\
"\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16"\
"\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17"\
"\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18"\
"\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19"\


#define BUFFER_DEFAULT_SIZE 4096


/* This software could be easy to hack because the size of the crypted file,
 * so the size of the original file is known
 */
int main(int argc, char **argv)
{
	if (argc > 1)
	{
		int fd, keyptr;
		char buffer_file[BUFFER_DEFAULT_SIZE];
		char *buffer_key;
		unsigned char keyc;
		ssize_t len,tmplen,size_key;

		if (argc > 2)
		{
			struct stat st;
			int fd_key,len_key;

			stat(*(argv + 2),&st);
			size_key = st.st_size;
			
			buffer_key = (char *)  malloc(size_key*sizeof(char));
			fd_key = open(*(argv + 2), O_RDONLY);
			len_key = 0;
			
			while(((len = read(fd_key,(buffer_key + len_key),
					size_key)) > 0)
				&& ((len_key += len) < size_key));
			close(fd_key);
		}
		else
		{
			char *tmpbuff;

			buffer_key = tmpbuff = (char *)
				malloc(sizeof(char) * BUFFER_DEFAULT_SIZE);

			while ((read(0,tmpbuff,1) > 0) && (*tmpbuff++ != '\n')
				&&(tmpbuff < (buffer_key+BUFFER_DEFAULT_SIZE)));
			
			size_key = (tmpbuff - buffer_key);
		}
		
		fd = open(*(argv + 1), O_RDONLY);
		
		keyptr = 0;
		keyc = *buffer_key;

		/* reading of "keyc" bytes affects the value of len 
		 * so the value of tmplen which is used to get a byte in 
		 * KEY_SOFT
		 */
		while ((len = read(fd,buffer_file,keyc)) > 0)
		{
			tmplen = len;
			while (tmplen--)
			{
				keyc = *(buffer_key + 
					(keyptr++ % size_key));
				
				/* using keyc, tmplen and keyptr values to get
				 * better results when using a very short key
				 */
				buffer_file[tmplen] ^= 
					(keyc ^ KEY_SOFT[(keyc*tmplen+keyptr)
							% sizeof(KEY_SOFT)]
					);
			}
			write(1,&buffer_file,len);
		}
		free(buffer_key);
		close(fd);
	}
	else
	{
		printf(	"usage: %s <file to crypt> [<key file>]\n"
			"\texample: %s file.txt file.key > file.crypt\n"
			"\tthen: %s file.crypt file.key > file.txt\n"
			,*argv,*argv,*argv);
	}
	return 0;
}

