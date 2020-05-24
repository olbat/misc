#include <stdio.h> // printf
#include <string.h> // memcpy
#include <sys/mman.h> // mmap, munmap

int main () {
	unsigned char code [] = { CODE };

	// allocate executable memory
	void* mem = mmap(NULL, sizeof(code), PROT_WRITE | PROT_EXEC,
		MAP_ANON | MAP_PRIVATE, -1, 0);

	// copy runtime code into allocated memory
	memcpy(mem, code, sizeof(code));

	// typecast allocated memory to a function pointer
	int (*func) () = mem;

	// call function pointer
	printf("%d + %d = %d\n", 8, 4, func(8, 4));

	// Free up allocated memory
	munmap(mem, sizeof(code));
}
