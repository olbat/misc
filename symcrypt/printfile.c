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
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PRINT_FORMAT "%.2x"
#define PRINT_DISPLAY(F,C) __extension__ \
({ \
	printf(F,C); \
	fflush(stdout); \
})

static int fd;

void stop(int no)
{
	close(fd);
}

int main(int argc, char **argv)
{
	if (argc > 3)
	{
		unsigned char c;
		int nbytes;
		ssize_t len;
		__extension__ char format[
			strlen(*(argv + 2)) + sizeof(PRINT_FORMAT) + 1
		];

		signal(SIGHUP,stop);
		signal(SIGTERM,stop);
		signal(SIGINT,stop);

		fd = open(*(argv + 1), O_RDONLY);
		nbytes = atoi(*(argv + 2));
		
		strcpy(format,*(argv + 3));
		strcat(format,PRINT_FORMAT);

		if (nbytes > 0)
		{
			while ((read(fd,&c,sizeof(c) > 0)) && (nbytes-- > 0))
				PRINT_DISPLAY(format,c);
			close(fd);
		}
		else
		{
			while (read(fd,&c,sizeof(c)) > 0)
				PRINT_DISPLAY(format,c);
		}

		puts("");
	}
	else
	{
		printf("usage: %s <file> <bytes to be read > <prefix format>\n"
			,*argv);
	}
	return 0;
}
