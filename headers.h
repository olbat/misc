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

#include <asm/types.h>
#ifndef LITTLE_ENDIAN
#define LITTLE_ENDIAN
#endif

struct ethernet_header
{
	__u8	destmac[6];
	__u8	sourcemac[6];
	__u16	proto;
};

__extension__ struct ipv4_header
{
#if defined(LITTLE_ENDIAN)
	__u8 iphdrlen:4,
	     version:4;
#elif defined(BIG_ENDIAN)
	__u8 version:4,
	     iphdrlen:4;
#else
#error "Please define LITTLE_ENDIAN or BIG_ENDIAN"
#endif
	__u8 tos;
	__u16 totlen;
	__u16 id;
	__u16 fragoffset;
	__u8 ttl;
	__u8 proto;
	__u16 ipchecksum;
	__u32 sourceaddr;
	__u32 destaddr;
};

__extension__ struct tcp_header
{
	__u16 sourceport;
	__u16 destport;
	__u32 seqnum;
	__u32 acknum;
#if defined(LITTLE_ENDIAN)
	__u16 res:4,
	      tcphdrlen:4,
	      fin:1,
	      syn:1,
	      rst:1,
	      psh:1,
	      ack:1,
	      urg:1,
	      ece:1,
	      ecn:1;
#elif defined(BIG_ENDIAN)
	__u16 tcphdrlen:4,
	      res:4,
	      ecn:1,
	      ece:1,
	      urg:1,
	      ack:1,
	      psh:1,
	      rst:1,
	      syn:1,
	      fin:1;
#else
#error "Please define LITTLE_ENDIAN or BIG_ENDIAN"
#endif

	__u16 window;
	__u16 tcpchecksum;
	__u16 urgptr;
};

struct pseudo_tcp_header 
{
 	__u32 sourceaddr;
	__u32 destaddr;
	__u8 zero;
	__u8 proto;
	__u16 tcplen;
};

struct data
{
	char *data;
	unsigned int len;
};
