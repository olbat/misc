# Create SSH tunnels using systemd units


## Table of contents
  * [Overview](#overview)
  * [Setup the SSH agent systemd unit](#setup-the-ssh-agent-systemd-unit)
  * [Setup the SSH-tunnel systemd unit](#setup-the-ssh-tunnel-systemd-unit)
  * [Create tunnels using systemd services](#create-tunnels-using-systemd-services)
  * [Examples](#examples)
    * [Create a tunnel to a web server on a machine that's only accessible by SSH](#create-a-tunnel-to-a-web-server-on-a-machine-thats-only-accessible-by-ssh)
    * [Create a tunnel to a MySQL service only accessible through an SSH bastion (directly)](#create-a-tunnel-to-a-mysql-service-only-accessible-through-an-ssh-bastion-directly)
    * [Create a tunnel to a MySQL service only accessible through an SSH bastion (using SSH)](#create-a-tunnel-to-a-mysql-service-only-accessible-through-an-ssh-bastion-using-ssh)
  * [Further reading](#further-reading)


## Overview
This systemd service scripts will allow you to create SSH tunnels in background
using systemd in user mode and a configuration file.


## Setup the SSH agent systemd unit
To be able to run SSH tunnels in background while using a password protected SSH
key to connect to the targeted host, we'll first have to setup an _ssh-agent_
(see [ssh-agent(1)](https://linux.die.net/man/1/ssh-agent)).

The agent will be run in background using a user _systemd service unit_ (see [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/systemd.service.html), [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/systemd.unit.html), [Arch Linux wiki page](https://wiki.archlinux.org/index.php/Systemd/User)).

```bash
# (create the systemd config directory if it does not exists)
mkdir -p ~/.config/systemd/user/

# create the ssh-agent.service unit
cat <<'EOF' > ~/.config/systemd/user/ssh-agent.service
[Unit]
Description=SSH key agent
Documentation=man:ssh-agent(1)
Wants=environment.target
Before=environment.target

[Service]
Type=forking
Environment="SSH_AUTH_SOCK=%t/ssh-agent.socket"
ExecStart=/usr/bin/ssh-agent -a $SSH_AUTH_SOCK
ExecStartPost=/bin/systemctl --user set-environment \
  SSH_AUTH_SOCK=${SSH_AUTH_SOCK}

[Install]
WantedBy=multi-user.target
EOF
```

Once it's done we can start the authentication agent:
```bash
systemctl --user start ssh-agent
```

Or even make it load at session opening:
```bash
systemctl --user enable ssh-agent
```
After that, we make the `$SSH_AUTH_SOCK` env variable be loaded at our shell
initialization (here [bash](https://www.gnu.org/software/bash/)):
```bash
echo 'export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"' >> ~/.bashrc
source ~/.bashrc
```

Finally we add our (default) private key identity to the authentication agent
using ssh-add (see [ssh-add(1)](https://linux.die.net/man/1/ssh-add)).
```bash
ssh-add
```
_Note:_ __it has to be done at every boot in order for the tunnels to work !__


## Setup the SSH-tunnel systemd unit
As for the [SSH authentication agent](#setup-the-ssh-agent-systemd-unit) service, we'll run our SSH tunnels ([ssh(1)](https://linux.die.net/man/1/ssh)) using a _systemd service unit_ but this unit will be instanciable (see [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/systemd.unit.html), [Lennart Poettering's blog](http://0pointer.de/blog/projects/instances.html), [Arch Linux wiki page](https://wiki.archlinux.org/index.php/Systemd#Using_units), [Fedoramagazine article](https://fedoramagazine.org/systemd-template-unit-files/)).

```bash
# (create the systemd config directory if it does not exists)
mkdir -p ~/.config/systemd/user/

# create the ssh-tunnel@.service unit
cat <<'EOF' > ~/.config/systemd/user/ssh-tunnel@.service
[Unit]
Description=SSH tunnel to %i
Documentation=man:ssh(1)
Wants=ssh-agent.service
After=network.target ssh-agent.service

[Service]
Type=simple
Environment="LOCAL_ADDR=127.0.0.1"
Environment="REMOTE_HOST=127.0.0.1"
EnvironmentFile=%h/.ssh/tunnels/%i
ExecStart=/usr/bin/ssh -NT ${TARGET} \
  -o ExitOnForwardFailure=yes -o ServerAliveInterval=60 \
  -L ${LOCAL_ADDR}:${LOCAL_PORT}:${REMOTE_HOST}:${REMOTE_PORT} ${SSH_OPTS}
RestartSec=10
Restart=on-success
RestartForceExitStatus=255

[Install]
WantedBy=multi-user.target
EOF
```


## Create tunnels using systemd services
We'll now create _systemd service instances_ to run our tunnels.

Our _ssh-tunnel_ service is going to look for it's configuration file into
the `~/.ssh/tunnels/` directory so we start with creating the directory:
```bash
mkdir -p ~/.ssh/tunnels/
```

We'll then have to create a configuration file for our tunnel:
```bash
cat <<'EOF' > ~/.ssh/tunnels/testtun
# This parameters will be used to run:
#     ssh ${TARGET} ${SSH_OPTS} \
#     -L ${LOCAL_ADDR}:${LOCAL_PORT}:${REMOTE_ADDR}:${REMOTE_PORT}

# The target of the SSH command
TARGET=user@hostname

# The local port to listen to
LOCAL_PORT=8080

# The remote port to forward
REMOTE_PORT=80

# The local address to listen to (default: _127.0.0.1_)
#LOCAL_ADDR=0.0.0.0

# The remote host to forward to (default: _127.0.0.1_)
#REMOTE_HOST=domain.tld

# Additional -custom- SSH options
#SSH_OPTS=-v
EOF
```

Finally we can run our _systemd service unit_ that will create the tunnel:
```bash
systemctl --user start ssh-tunnel@testtun
```

Or make it load a session loading:
```bash
systemctl --user enable ssh-tunnel@testtun
```

_Note:_ make sure your SSH authentication agent has been loaded properly using
`ssh-add`, the tunnel will not work without it

We can check the tunnel's status using:
```bash
systemctl --user status -l ssh-tunnel@testtun
```

Or list the _systemd services_ of current user:
```bash
systemctl --user list-units --type=service
```


## Examples

### Create a tunnel to a web server on a machine that's only accessible by SSH

Let's create a configuration file to access to the web server (_80_ port)
of the _www.privatecloud.domain.tld_ machine and make the tunnel accessible to
other machines over the network:

```bash
cat <<'EOF' > ~/.ssh/tunnels/privatecloud-www
TARGET=user@www.privatecloud.domain.tld
LOCAL_ADDR=0.0.0.0
LOCAL_PORT=8080
REMOTE_PORT=80
EOF
```

Then start the tunnel and make it load at session loading:
```bash
systemctl --user start ssh-tunnel@privatecloud-www
systemctl --user enable ssh-tunnel@privatecloud-www
```

We can now connect to the web server using:
```bash
curl http://127.0.0.1:8080/
```

or (from another machine that's in the same network):
```bash
curl http://mymachine.domain.lan:8080/
```

### Create a tunnel to a MySQL service only accessible through an SSH bastion (directly)

Let's create a configuration file to access to the MySQL server (_3306_ port)
of the _mysql.privatecloud.domain.tld_ machine that's only through the
_access.privatecloud.domain.tld_ bastion:

```bash
cat <<'EOF' > ~/.ssh/tunnels/privatecloud-mysql
TARGET=user@access.privatecloud.domain.tld
LOCAL_PORT=3306
REMOTE_PORT=3306
REMOTE_HOST=mysql.privatecloud.domain.tld
EOF
```

Then start the tunnel:
```bash
systemctl --user start ssh-tunnel@privatecloud-mysql
```

We can now connect to the mysql.privatecloud's MySQL service using:
```bash
mysql -h 127.0.0.1
```

### Create a tunnel to a MySQL service only accessible through an SSH bastion (using SSH)

In this example, we want to create the same tunnel than the one in the
[previous example](#create-an-ssh-tunnel-to-a-mysql-service-only-accessible-through-an-ssh-bastion-directly)
but this time the MySQL service is not accessible directly from the bastion
(on port _3306_).

Fortunately, the _mysql.privatecloud_ machine is accessible from the bastion
using SSH so we can create a tunnel using an ssh jump (see
[ssh(1)](https://linux.die.net/man/1/ssh),
[wikibooks article](https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Proxies_and_Jump_Hosts)):
```bash
cat <<'EOF' > ~/.ssh/tunnels/privatecloud-mysql
TARGET=mysql.privatecloud.domain.tld
LOCAL_PORT=3306
REMOTE_PORT=3306
REMOTE_HOST=127.0.0.1
SSH_OPTS="-J access.privatecloud.domain.tld:22"
EOF
```

Then start the tunnel:
```bash
systemctl --user start ssh-tunnel@privatecloud-mysql
```

We can now connect to the _mysql.privatecloud.domain.tld_'s MySQL service using:
```bash
mysql -h 127.0.0.1
```


## Further reading
- systemd's [unit](https://www.freedesktop.org/software/systemd/man/systemd.unit.html) and [service](https://www.freedesktop.org/software/systemd/man/systemd.service.html) and manpages
- Arch Linux wiki's [Systemd](https://wiki.archlinux.org/index.php/Systemd), [Systemd/User](https://wiki.archlinux.org/index.php/Systemd/User) and [SSH_keys](https://wiki.archlinux.org/index.php/SSH_keys) pages
- DigitalOcean's [introduction to systemd units](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)
