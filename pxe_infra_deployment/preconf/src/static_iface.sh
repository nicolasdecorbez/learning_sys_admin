#!/bin/bash

function static_iface() {
  iface_conf=$(cat /etc/network/interfaces | grep -e "iface $interface" | cut -d " " -f 4);       # On récupère la configuration actuelle de l'interface

  if [[ $iface_conf != "static" ]]; then
    sed -i "s/iface $interface inet dhcp/iface $interface inet static/" /etc/network/interfaces;  # On modifie l'interface en remplaçant dhcp par static
    echo "-> Interface $interface updated.";
    echo $separator;
  fi
}
