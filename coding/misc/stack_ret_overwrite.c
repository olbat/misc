#include <stdio.h>
#include <limits.h>

void fun()
{
	char c;
	char *ret;

	ret = &c + sizeof(c) + 2*(__WORDSIZE/8); // FP + RET
	*ret += 0x7; // see gdb disassemble
}

int main()
{
	int x;

	x = 1;
	fun();
	x = 2;

	printf("%d\n",x);

	return 0;
}
