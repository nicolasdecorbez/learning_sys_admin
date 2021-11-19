# Local Network

To ensure a proper isolation of our subnet, we created a subnet with 2 virtual machines : 
- a `gateway`, handling `ip-forwarding`, `iptables`, etc.
- a `manager`, to setup DHCP for new clients and *netboot*

## Gateway configuration

As a `gateway` for our subnet, we created a *Debian 10* virtual machine with two networks interfaces : 
- a *bridge*, to have an internet connection
- a *host_only*, to redirect this connection to every machines on this subnet

### Interfaces configuration

Edit the `/etc/network/interfaces` file to setup your **bridge** interface (here *enp0s8*) into *dhcp* mode, and the **host-only** one into *static* mode, associated to the `192.168.100.1` address :
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
    address 192.168.100.1
    netmask 255.255.255.0

# The secondary network interface : bridge
allow-hotplug enp0s8
iface enp0s8 inet dhcp
```

### IP forwarding

Configure the **ip-forwarding** by uncommenting the following line into the `/etc/sysctl.conf` file :
```
net.ipv4.ip_forward = 1
```

### `iptables`

Assuming your **bridge** network interface is still `enp0s8`, you can configure your **iptable** like this :
```console
iptables -t nat -A POSTROUTING ! -d 192.168.100.0/24 -o enp0s8 -j MASQUERADE
```

> `192.168.100.0/24` is the network range where I want to redirect internet connection.

Then install the `iptables-persistent` package and run this command to save your **iptables** :
```
iptables-save > /etc/iptables/rules.v4
```

We can now configurate our *manager* VM.


## Manager configuration

Now that we can access to the internet, we need to setup the DHCP over our network.

So, we create another *Debian 10* VM with only one network interface (*host-only*)

### Interface

Modify the network interface configuration into `/etc/network/interfaces` like following :
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
    address 192.168.100.2
    netmask 255.255.255.0
    gateway 192.168.100.1
```
> Don't forget to add the gateway IP address to this configuration

# DHCP Server

First install the *DHCP* server : `apt install isc-dhcp-server`

Then modify `/etc/dhcp/dhcpd.conf` by adding :

- A **subnet** :
```
subnet 192.168.100.0 netmask 255.255.255.0 {
	option routers 192.168.100.1;
  range 192.168.100.100 192.168.100.200;
}
```

- A **group** :
```
group {
  next-server 192.168.100.3  # adresse de notre server PXE, que nous allons configurer plus tard
  host tftpclient {
    hardware ethernet <mac-address>;    # On configure l'adresse mac de la VM cible.
    filename "pxlinux.0";               # On rentre les informations de notre PXE
  }
}
```

- And few other modifications like :
  - `option domain-name "example.org";` : comment this line.
  - `option domain-name-server ns1.example.org, ns2.example.org;` becomes `option domain-name-server 8.8.8.8, 8.8.4.4`
  - uncomment the `#authoritative` option
  - and add the following options : `allow booting;` et `allow bootp;`

Restart the VM and you are ready to go !

Our network is now ready to accept more servers, like our PXE and NFS ones. Let's configure them.
