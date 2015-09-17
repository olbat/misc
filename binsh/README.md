# binsh - obfuscate shell scripts

## Overview
This tool allows to obfuscate shell scripts by compiling, encrypting and passphrase-protect them.

The script is included in the compiled binary as a constant so when you run the binary, the script is executed using `/bin/sh -c --`.

The running environment (arguments, environement variables, fds) is forwarded to the script.

## How does it work
The main idea is not to be able to determine what does the script do just by opening the script file.

First of all, the script is included as a constant in a compiled program so it's harder to understand what it does by just opening the file.

The script is encrypted using a simple key-based symetric encryption algorithm before the compilation so it's not possible to determine what the binary file does using softwares such as `strings`.

In the end, the script is decrypted at run time using the key in order to avoid the binary to be analysed using softwares such a `strace` (without the key you can't run the script).

## Examples

### Compile then run a script using a passphrase
```bash
./build.sh script.sh my_p4ssphras3 script
env=123 ./script my_p4ssphras3 --opt 456
```

### Compile then run a script using a key file
```bash
dd if=/dev/urandom of=keyfile bs=512 count=1
./build.sh script.sh - script < keyfile
env=123 ./script - --opt 456 < keyfile
```
