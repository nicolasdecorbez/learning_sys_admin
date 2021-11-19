# PXE configuration

A Preboot eXecution Environment (PXE) server offers the needed network resources to client PCs that were configured to boot from one of its network devices instead of booting from the classic mass storage options (SSD/HDD/DVD).

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
    address 192.168.100.3
    netmask 255.255.255.0
    gateway 192.168.100.1
```

`192.168.100.3` will be its static IP into our sub-network.

## Server configuration

First, install the two following packages on the PXE VM : `apt install tftpd-hpa di-netboot-assistant`

- `tftpd-hpa` (Travial FTP) : a basic FTP server to seend our preseed to our new VMs.
- `di-netboot-assistant` : all necessary tools to download required files for boot.

### `di-netboot-assistant`

Configure your assistant by editing `/etc/di-netboot-assistant/di-netboot-assistant.conf`, line `TFTP_ROOT` :
```
[...]
TFTP_ROOT=/srv/tftp
[...]
```

Then download a fresh stabe version of debian buster : `di-netboot-assistant install stable`.

### *preseeds*

First, you will have to prepare your root into `/srv/tftp` :
```
cp -r /srv/tftp/d-i/n-a/* /srv/tftp/
```

Then create a new directory, `preseed_templates`. We will store all our preseed-templates into this one.

- [`standard.cfg`](preseed_templates/standard.cfg) the bare minimum for client to interact with servers (*NFS*, *TFTP*, etc.).
- [`vps-ecom.cfg`](preseed_templates/vps-ecom.cfg) ecom-like environment following **LAMP** ecosystem.

To choose a specific template, run the following command:
```
cp /srv/tftp/preseed_templates/<template> /srv/tftp/preseed.cfg
```

## Boot configuration

We start by creating a backup of `/srv/tftp/pxelinux.cfg/default` :
```
mv /srv/tftp/pxelinux.cfg/default /srv/tftp/pxelinux.cfg/default.old
```

Then we inject [our custom configuration](pxelinux.cfg/default) into `/srv/tftp/pxelinux.cfg/default`. It will automatically load the boot configuration and the preseed to configure the new machine.
