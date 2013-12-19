/*
 * Copyright (C) 2013 Sarzyniec Luc <contact@olbat.net>
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

#include <unistd.h>
#include <stdio.h>
#include <string.h>

extern char **environ;

/* #define SCRIPT "..." */

int main(int argc, char **argv)
{
	if (argc > 1)
        {
	        int fds[2];
	        unsigned int i;
	        size_t len;
                char *args[argc+1];
	        char *key;

	        pipe(fds);
	        close(STDIN_FILENO);
	        dup2(fds[0], STDIN_FILENO);

	        args[0] = "/bin/sh";
	        args[1] = "-s";
	        for (i=2;i < argc;i++)
	        	args[i] = argv[i];
	        args[i] = NULL;

	        key = argv[1];
	        len = strlen(key);
	        for (i=0;i < (sizeof(SCRIPT)-1);i++)
	        	write(fds[1],&(char){SCRIPT[i]^key[(i+key[i%len])%len]},1);
	        close(fds[1]);

	        execve(args[0], args, environ);

	        perror("execve");
	        return 1;
        }
        else
        {
		printf("usage: %s <key> <args>\n",*argv);
                return 1;
        }
}
