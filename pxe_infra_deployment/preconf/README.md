# Script de pré-configuration

This script configure and install all required files on new VMs.

- *hostname* modification
- *prompt* modification
- `root` password modification
- create a new user
- set IP address as `static`
- *MOTD* configuration
- add the *SSH key* of a distant server
- disable `root` login by *SSH*
- *SSH port* modification
- `sudo` configuration
- `fail2ban` configuration
- `vim`, `rsync` & `wget` installation
- remove installation scripts 

> you can access to this script on the **NFS Server** : `/media/nfs/preconf`

Please be aware that you have to run this script with `root` privileges.

## Configuration

Into `src/conf.d` directory, you will find 2 configuration files : **`user.conf`** et **`root.conf`**.

**`user.conf`** : configure `username` and `password` for the new user.
```bash
# -------------------------------------- #
# Configuration file for user_creator.sh #
# -------------------------------------- #

# Set-up the customer username
USERNAME=client

# Set-up the customer password
PASSWORD=client
```

**`root.conf`** : configure the new root password.
```bash
# ---------------------------------------------- #
# Configuration file for root_passwd_modifier.sh #
# ---------------------------------------------- #

# Set-up the new root password
ROOT_PASSWORD=toor
```

## Installation

Login with the default user (`administrator` for example), then login as **`root`** with `su`.
```
Debian GNU/Linux 10 debian tty1

debian login: administrator
Password:

[...]

administrator@debian:~$ su
Password:
root@debian:/home/administrator#
```

As `root`, go to `preconf`, then enter :
```console
# cd preconf
# bash preconf.sh
```