#!/bin/bash

function which_interface() {    # Permet de déterminer quelle est l'interface de base. Sous VirtualBox : enp0s3 / Sous VMWare : ens33
  interface=$(ip addr | grep -e "2: en" | cut -d ":" -f 2 | sed 's/ //');
}

function modify_host() {        # On modifie le fichier /etc/hosts pour que sudo marche correctement.
  local ac_host=$(cat /etc/hosts | grep 127.0.1.1 | cut -d$'\t' -f 2);
  if [[ $ac_host != $new_hostname ]]; then
    sed -i "s/127.0.1.1\t$ac_host/127.0.1.1\t$new_hostname/" /etc/hosts
    echo "-> /etc/hosts changed.";
    echo $separator;
  fi
}

function hostname_mod() {       # Changement du hostname s'il n'est pas égal à vps-<4 derniers chiffres de l'adresse mac>
  local hostname=$(hostname);   # On récupère le hostname actuel
  new_hostname=vps-$(ip addr show $interface | grep ether | cut -d ' ' -f 6 | cut -c 13- | sed 's/\://');
  which_interface;
  if [[ $hostname != "vps-$(ip addr show $interface | grep ether | cut -d ' ' -f 6 | cut -c 13- | sed 's/\://')" ]]; then   # S'il n'est pas égal à celui désiré, on le change
    echo "-> The program will now modify the hostname of your machine.";
    hostnamectl set-hostname $new_hostname;
    echo "-> Hostname changed.";
  fi
  modify_host;
}
