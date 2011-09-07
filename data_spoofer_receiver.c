/*
 * Copyright (C) 2006, 2007 Sarzyniec Luc <olbat@xiato.com>
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

#include <linux/if_ether.h>
#include <sys/socket.h>
#include <string.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <malloc.h>
#include <stdlib.h>
#ifndef _I386_TYPES_H 
#include <asm/types.h>
#endif
#include <fcntl.h>
#include <unistd.h>
#include "headers.h"

#define DATAGRAM_SIZE 4096

static	char *datagram;
static	struct ipv4_header *iph;
static	struct tcp_header *tcph;
static 	__u16 sourceport,destport;

int read_seqdata(int fd,char *buff,__u32 *seqnum,int *num)
{
	int end;
	
	end = 1;
	iph = (struct ipv4_header *) (datagram + sizeof(struct ethernet_header));
	
	if (iph->proto == IPPROTO_TCP)
	{
		tcph = (struct tcp_header *) (datagram
			+ sizeof(struct ethernet_header)
			+ sizeof(struct ipv4_header));
		if ((tcph->sourceport == sourceport) 
			&& (tcph->destport == destport) && (tcph->ack == 1))
		{
			if (num)
			{
				__u32 tmpu;
				char tmpc[4]; 
				tmpu = (ntohl(tcph->acknum) -1);
				
				memcpy(tmpc,&tmpu,sizeof(__u32));
				
				*num = *tmpc;
				memcpy(seqnum,tmpc+sizeof(char),sizeof(__u32)-1);
			}
			else
			{
				/* -1 dues incrementation of the seqnum
				 * (TCP protocol)
				 */

				*seqnum = (ntohl(tcph->acknum) - 1);
			}
			
			/* printf("RECEIVED_DATA %#x\n",*seqnum); */
			
			end = 0;
		}
	}
	else
	{
		end = -1;
	}
	return end;
}

char *read_data(int fd,char *buffer,int size)
{
	char *ptr;
	__u32 wbuffer;
	int num;

	ptr = buffer;
	
	while (((read(fd,datagram,DATAGRAM_SIZE) > 0) && (size > 0)))
	{
		if (!read_seqdata(fd,datagram,&wbuffer,&num))
		{
			memcpy(ptr+(num*(sizeof(__u32)-1)),&wbuffer,
				sizeof(__u32)-1);
			size = size - (sizeof(__u32) -1);
		}
	}
	return buffer;
}

int main(int argc,char **argv)
{
	if (argc > 3)
	{		
		char end;
		char *filebuffer;
		__u32 seqnum;
		int sockfd,fd,wdata;

		sourceport = (__u16) htons(atoi(argv[3]));
		destport = (__u16) htons(atoi(argv[2]));
		
		datagram = (char *) malloc(DATAGRAM_SIZE * sizeof(char));
		iph = (struct ipv4_header *) datagram;		
		tcph = (struct tcp_header *) (datagram
			+ sizeof(struct ipv4_header));

		memset(datagram,0,DATAGRAM_SIZE);

		/* if ((sockfd = socket(AF_INET,SOCK_RAW,IPPROTO_TCP)) < 0) */
		if ((sockfd = socket(PF_PACKET,SOCK_RAW,htons(ETH_P_ALL))) < 0)	
		{
			perror("socket");
			exit(1);
		}

		fputs("start listening ...\n",stdout);
		
		end = 0;
		while (!end)
		{
			if (read(sockfd,datagram,DATAGRAM_SIZE) < 0)
			{
				perror("read");
				end = 1;
			}

			if (!read_seqdata(sockfd,datagram,&seqnum,0))
			{
				if (!seqnum)
				{
					fputs("----receiving data----\n",stdout);
					
					fd = open(argv[1],O_CREAT|O_WRONLY);
					read(sockfd,datagram,DATAGRAM_SIZE);
					while (read_seqdata(sockfd,datagram,
						&seqnum,0))
					{
						read(sockfd,datagram,
							DATAGRAM_SIZE);
					}
					while (seqnum)
					{
						wdata = (int) seqnum;
						filebuffer = (char *) malloc(
							wdata * sizeof(char));
						
						filebuffer = read_data(sockfd,
							filebuffer,wdata);
						fwrite(filebuffer,sizeof(char),
							wdata,stdout);
						write(fd,filebuffer,wdata);
						
						while (read_seqdata(sockfd,
							datagram,&seqnum,0))
						{
							read(sockfd,datagram,
								DATAGRAM_SIZE);
						}
						free(filebuffer);
					}
					close(fd);
					end = 1;
				}
			}
		}
		close(sockfd);
		
		free(datagram);
		
		fputs("----------------------\nfile received.\n",stdout);
	}
	else
	{
		fprintf(stdout,	"usage : %s <output file name> <source port> "
				"<destination port>\n"
			       	"(use the same port source and destination as "
				"the sender)\n",argv[0]);
	}

	return 0;
}
