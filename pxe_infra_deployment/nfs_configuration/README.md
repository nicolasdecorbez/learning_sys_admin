# NFS Server configuration

We will now configure our `nfs` vm to setup our **NFS** (*Network File System*) server on our local network.

## Networking

We first configure our interface as **host-only**, then we modify `/etc/network/interfaces` :
```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface : host-only
allow-hotplug enp0s3
iface enp0s3 inet static
    address 192.168.100.4
    netmask 255.255.255.0
    gateway 192.168.100.1
```

`192.168.100.4` will be its static IP into our sub-network.

## Server configuration

We can now install all necessary tools to configure our server : `apt install nfs-kernel-server`

Then configure the service to launch at machine startup : `systemctl enable --now nfs-server.service`

## Share configuration

First create the `/media/nfs` folder as our shared folder, then modify `/etc/exports` to enable sharing :
```
/media/nfs           192.168.100.0/24(rw,sync,no_root_squash)
```

Some explications about previous line: 

- `/media/nfs` : the path of the folder you want to share.
- `192.168.100.0/24` : allowed IPs to access this folder. You can either specify one specific address or a range of IPs.
- *options* :
  - `rw` : permissions on our shared folder.
  - `sync` : to avoid data corruption, check modifications before writing to the server.
  - `no_root_squash` : avoid root user mapping to an anonymous one (recommended).

Once configured, we apply our configuration : `exportfs -a`
Then we restart the service : `systemctl restart nfs-server.service`

## Client configuration

To access this file-share, you must install the `nfs-common` package : `apt install nfs-common`

Then mount your share on your local filesystem : `mount -t nfs 192.168.100.4/media/nfs <dest>`
