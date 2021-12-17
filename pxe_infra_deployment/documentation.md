# Documentation

Here is the documentation to create a new client virtual machine.

## Setup

### Virtual Machine

Create a VirtualBox virtual machine with following requirements:

- **CPU :** 1 Cœur
- **RAM :** 2 Go
- **OS :** Debian
- **Networking :** Host-Only
- **Boot order :** only "Network"

Then go to *Configuration -> Network -> Advanced* and store the **MAC** address.

### Preseed

Into the **PXE** vm, choose one *preseed* based on the type of VM you want to deploy. 

> More informations [here](pxe_configuration/README.md).

### Add the MAC address

Into the **Manager** VM, edit the `/etc/dhcp/dhcpd.conf` and modify the **MAC** address on the line `hardware ethernet <mac-address>`.

### Change client informations

Into the **NFS** VM, edit the files into the `/media/nfs/preconf/conf.d` directory :

- **`user.conf`** : client informations
- **`root.conf`** : root informations

> More information [here](preconf/README.md).

## Install Debian from PXE server

> `gateway`, `manager` and `pxe` VMs must run.

We can lauch our client VM ; the installation will start automatically.

After the VM has restarted, edit the **Boot Order** and enable "Hard-Drive", then start the VM.

## First connection

You can login with your root used, and run the following commands :
```console
# mount -t nfs 192.168.100.4:/media/nfs /tmp && cp -r /tmp/preconf /root/ 
# bash /root/preconf/preconf.sh
```

> More informations [here](preconf/README.md).
