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

#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <malloc.h>

#define DOMAINNAME "xiato.com"
#define DNSDATAGRAM_SIZE 4096
#define DNSPORT 53
#define DNSIP "213.246.63.35"
#define _BIG_ENDIAN
#define DNSDEBUG 

/* DNS HEADER */
struct dnshdr 
{
	unsigned short id;
	/* switch between little and big edian because of the host byte order */
#ifdef _LITTLE_ENDIAN
	unsigned char qr:1,
		      opcode:4,
		      aa:1,
		      tc:1,
		      rd:1;
	unsigned char ra:1,
		      z:3,
		      rcode:4;

#endif 
#ifdef _BIG_ENDIAN
	unsigned char rd:1,
		      tc:1,
		      aa:1,
		      opcode:4,
		      qr:1;
	unsigned char rcode:4,
		      z:3,
		      ra:1;
#endif
	unsigned short qdcount;
	unsigned short ancount;
	unsigned short nscount;
	unsigned short arcount;
};

/* RESSOURCE RECCORD FORMAT */
struct rrhdr
{
	/* struct rr_name name; */
	unsigned short type;
	unsigned short class;
	unsigned int ttl;
	unsigned short rdlength;
	/* struct rr_rdata rdata; */
};

/* QUESTION SECTION FORMAT */
struct dnshdr_name
{
	char *value;
	unsigned short size;
};

struct qshdr
{
	/* struct qs_name qname; */
	unsigned short qtype;
	unsigned short qclass;
};

void get_qname(char *name,struct dnshdr_name **qname)
{
	int i,current;
	short totsize;
	char c;
	char *end;
	/* ... verifs args ... */
	c = name[0];
	totsize = (short) c;
	i = 0;
	current = 0;
	end = (char *) malloc(sizeof(char)*64); /* max size of a domain name */
	while (c != 0)
	{
		if (i == (totsize + 1))
		{
			c = name[totsize+1];
			totsize = (short) totsize + c +1;
			end[current] = '.';
			current++;
		}
		else
		{
			end[current] = name[i];
			current++;
		}
		i++;
	}
	(*qname)->value = (char *) malloc(sizeof(char)*totsize);
	memcpy((*qname)->value,end,totsize);
	(*qname)->size = totsize;
}

void print_rdata(struct dnshdr_name *rname,struct rrhdr *rrh, char *rdata) {
	unsigned short type,class;
	struct dnshdr_name *name;
	/* ... verifs args ... */
	name = (struct dnshdr_name *) malloc(sizeof(struct dnshdr_name));
	type = ntohs(rrh->type);
	class = ntohs(rrh->class);
	if (class == 1)
		fputs("IN ",stdout);
	else if (class == 2)
		fputs("CS ",stdout);
	else if (class == 3)
		fputs("CH ",stdout);
	else if (class == 4)
		fputs("HS ",stdout);
	else 
		fputs("UNKNOWN_CLASS ",stdout);
	if (type == 1)
	{
		fprintf(stdout,"A %s\n",inet_ntoa(*((struct in_addr *)rdata)));
	}
	else
	{
		if (type == 2)
			fputs("NS ",stdout);
		else if (type == 3)
			fputs("MD ",stdout);
		else if (type == 4)
			fputs("MF ",stdout);
		else if (type == 5)
			fputs("CNAME ",stdout);
		else if (type == 6)
			fputs("SOA ",stdout);
		else if (type == 7)
			fputs("MB ",stdout);
		else if (type == 8)
			fputs("MG ",stdout);
		else if (type == 9)
			fputs("MR ",stdout);
		else if (type == 10)
			fputs("NULL ",stdout);
		else if (type == 11)
			fputs("WKS ",stdout);
		else if (type == 12)
			fputs("PTR ",stdout);
		else if (type == 13)
			fputs("HINFO ",stdout);
		else if (type == 14)
			fputs("MINFO ",stdout);
		else if (type == 15)
			fputs("MX ",stdout);
		else if (type == 16)
			fputs("TXT ",stdout);
		else 
			fputs("UNKNOWN_TYPE ",stdout);
		fwrite(rname->value,sizeof(char),rname->size,stdout);
		get_qname(rdata,&name);
		fwrite(name->value,sizeof(char),name->size,stdout);
		fputc('\n',stdout);
	}
}

#ifdef DNSDEBUG
int print_rrhdr(struct dnshdr_name *name,struct rrhdr *rrh,char *rdata, char *rrname)
{
	/* ... verfis args ... */
	fprintf(stdout,"[RESOURCE RECORD : %s]\n",rrname);
	fputs(" name:",stdout);
	fwrite(name->value,sizeof(char),name->size,stdout);
	fprintf(stdout,"type:%d class:%d ttl:%d rdlength:%d\n",ntohs(rrh->type),ntohs(rrh->class),ntohl(rrh->ttl),ntohs(rrh->rdlength));
	print_rdata(name,rrh,rdata);
	return 0;
}

int print_dnshdr(struct dnshdr *dnsh, char *name)
{
	/* ... verifs args ... */
	fprintf(stdout,"\n[[DNS DATAGRAM : %s]]\n",name);
	fputs("[HEADERS]\n",stdout);

	fprintf(stdout," id:%hd qr:%d opcode:%d aa:%d tc:%d rd:%d ra:%d z:%d rcode:%d\n qdcount:%hd ancount:%hd nscount:%hd arcount:%hd\n",dnsh->id,dnsh->qr,dnsh->opcode,dnsh->aa,dnsh->tc,dnsh->rd,dnsh->ra,dnsh->z,dnsh->rcode,ntohs(dnsh->qdcount),ntohs(dnsh->ancount),ntohs(dnsh->nscount),ntohs(dnsh->arcount));
	
	return 0;
}

int print_qshdr(struct dnshdr_name *qname,struct qshdr *qsh)
{
	/* ... verifs args ... */
	fputs("[QUERY]\n",stdout);
	fputs(" qname:",stdout);
	fwrite(qname->value,sizeof(char),qname->size,stdout);
	fprintf(stdout," qtype:%d qclass:%d\n",ntohs(qsh->qtype),ntohs(qsh->qclass));

	return 0;
}
#endif

void set_qname(char *name,struct dnshdr_name **qname)
{
	int i,totsize,currentsize, namesize;
	namesize = strlen(name);
	char *end = (char *) malloc(sizeof(char)*(namesize + 2)); /* +1 for the \0 and +1 for the first token size */
	/* ... verifs args ... */
	end[namesize + 1] = 0; /* the last byte of the qname entry must be at zero */
	(*qname)->size = (short) namesize + 2;
	currentsize = 0;
	totsize = namesize;
	for(i = (namesize - 1); i >= 0; i--)
	{
		if (name[i] == '.')
		{
			end[totsize] = currentsize;
			currentsize = 0;

		}
		else
		{
			end[totsize] = name[i];
			currentsize++;
		}
		totsize--;
	}
	end[totsize] = currentsize;
	(*qname)->value = end;
}

void get_name(char *name,struct dnshdr_name **qname)
{
	(*qname)->size = 2;
	(*qname)->value = (char *) malloc((*qname)->size*sizeof(char));
	memcpy((*qname)->value,name,(*qname)->size);
}

int main(int args, char **argv) {
	char datagram[DNSDATAGRAM_SIZE];
	char recv_datagram[DNSDATAGRAM_SIZE];
	char *recv_current;
	char *send_current;
	int re, reclen;
	unsigned char qs_name_size;
	char *dn;
	int sockfd;
	struct sockaddr_in sock, rec;
	struct dnshdr *dnsh;
	struct rrhdr * rrh;
	struct dnshdr_name *qsh_name;
	struct dnshdr_name *rrh_name;
	struct qshdr *qsh;

	if (args > 1)
	{
		dn = argv[1];
	}
	else
	{
		dn = DOMAINNAME;
	}
	
	fprintf(stdout,"Resolving %s ...\n",dn);
	
	send_current = datagram;
	dnsh = (struct dnshdr *) datagram;		
	
	if((sockfd = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)) < 0)
	{
		perror("socket");
	}

	sock.sin_family = AF_INET;
	sock.sin_port = htons(DNSPORT);
	sock.sin_addr.s_addr = inet_addr(DNSIP);

	memset(send_current,0,DNSDATAGRAM_SIZE);

	dnsh->id = 8147;
	dnsh->qr = 0; /* request */
	dnsh->opcode = 0; /* request type Query */
	dnsh->aa = 0;
	dnsh->tc = 0;
	dnsh->rd = 0;
	dnsh->ra = 0;
	dnsh->z = 0;
	dnsh->rcode = 0; /* no error */
	dnsh->qdcount = htons(1); /* 1 name in the question request */
	dnsh->ancount = 0;
	dnsh->nscount = 0;
	dnsh->arcount = 0;

	qs_name_size = strlen(dn); /* size of the domain name (without the '\0') */
	send_current[sizeof(struct dnshdr)] = strlen(dn);
	send_current = send_current + sizeof(struct dnshdr); 
	qsh_name = (struct dnshdr_name *) malloc(sizeof(struct dnshdr_name));
	memset(qsh_name,0,sizeof(struct dnshdr_name));
	set_qname(dn,&qsh_name);
	memcpy(send_current,qsh_name->value,qsh_name->size);
	send_current = send_current + qsh_name->size; 
	qsh = (struct qshdr *) (send_current);
	qsh->qtype = htons(1); /* type is A */
	qsh->qclass = htons(1); /* class is IN */


	if (sendto(sockfd, datagram,(sizeof(struct dnshdr) + 1 + strlen(dn) + 1 + 4), 0, (struct sockaddr *)&sock, sizeof(sock)) < 0)
	{
		perror("sendto");
	}
	else
	{
		fputs("->Request sent\n",stdout);
#ifdef DNSDEBUG
	print_dnshdr(dnsh,"request");
	print_qshdr(qsh_name,qsh);	
#endif
	}
	reclen = sizeof(rec);
	re = 0;
	if ((re = recvfrom(sockfd, recv_datagram, DNSDATAGRAM_SIZE,0,(struct sockaddr *)&rec,(socklen_t *)&reclen)) < 0)
	{
		perror("recvfrom");
	}
	else
	{
		recv_current = recv_datagram;
		dnsh = (struct dnshdr *) recv_datagram;
		fprintf(stdout,"\n<-Received %d Bytes\n",re);
		fflush(stdout);
#ifdef DNSDEBUG
		print_dnshdr(dnsh,"answer");
#endif
		recv_current = recv_current + sizeof(struct dnshdr);
		if (dnsh->ancount > 0)
		{
			free(qsh_name);
			qsh_name = (struct dnshdr_name *) malloc(sizeof(struct dnshdr_name));	
			get_qname(recv_current,&qsh_name);
			qsh = (struct qshdr *) (recv_current + (qsh_name->size) + 1);
			recv_current = (char *) recv_current + qsh_name->size + sizeof(struct qshdr) + 1;
			rrh_name = (struct dnshdr_name *) malloc(sizeof(struct dnshdr_name));
			get_name(recv_current,&rrh_name);
			recv_current = recv_current + rrh_name->size;
			rrh = (struct rrhdr *) recv_current;
			recv_current = recv_current + sizeof(struct rrhdr) -2;
#ifdef DNSDEBUG
			print_qshdr(qsh_name,qsh);
			print_rrhdr(rrh_name,rrh,recv_current,"ANSWER");
#else
			fputs("[Answer]\n",stdout);
			print_rdata(rrh_name,rrh,recv_current);
#endif
			recv_current = recv_current + rrh->rdlength;
		}
		
	}
	return 0;
}

