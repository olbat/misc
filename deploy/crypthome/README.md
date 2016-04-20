# Crypt /home scripts

## About
This scripts allow to create an encrypted /home partition and load it properly
at system's boot.

A warning message will be displayed at user's login when the encrypted /home
partition isn't mounted.


## Run the scripts
0. _[optional]_ Generate a key file containing a random passphrase: `dd if=/dev/urandom of=keyfile bs=1M count=4`
1. Edit the `crypthome.env` file to fit your needs
2. Create the encrypted partition `./create-homepart.sh /path/to/crypthome.env`
3. _[optional]_ Deploy system's files
4. Configure the system `./config-homepart.sh /path/to/crypthome.env`
5. _[optional]_ Reboot the system
6. Decrypt /home using the key file


## Run with [Kadeploy3](http://kadeploy3.gforge.inria.fr/)

```bash
kadeploy3 -m NODES -e IMAGE -k --custom-steps kadeploysteps-crypthome.yml
```


## On [Grid'5000](https://www.grid5000.fr/)
```bash
oarsub -I -t deploy -t destructive -l nodes=NUMBER,walltime=TIME
kadeploy3 -f $OAR_NODEFILE -e IMAGE -k --custom-steps kadeploysteps-crypthome.yml
```
__Note__: on unsecure and versatile environments, a key file should be generated at each run and deleted after the /home partition is mounted
