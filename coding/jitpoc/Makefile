CC=gcc
FUNC=add

define disassemble
	objdump -j .text -d $(1) -M intel \
	| awk -v RS= '/^[[:xdigit:]]+ <$(FUNC)>/' \
	| tail -n +2
endef

define generate_opcodes
	$(call disassemble,$(1)) \
	| cut -d$$'\t' -f2 \
	| sed -e 's/\([[:xdigit:]]\{2\}\)/0x\1,/g' \
	| paste -s -
endef

jit: $(FUNC).o jit.c
	@gcc -DCODE="`$(call generate_opcodes,$<)`" $@.c -o $@

print_opcodes: $(FUNC).o
	@$(call generate_opcodes,$<)

print_disassembled: $(FUNC).o
	@$(call disassemble,$<)

$(FUNC).o: $(FUNC).c
	$(CC) -c $< -o $@

.PHONY: print_disassembled print_opcodes
