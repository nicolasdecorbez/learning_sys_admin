#!/bin/bash

function ssh_port_modifier() {
  ssh_port_conf=$(cat /etc/ssh/sshd_config | grep -e "Port ");                  # On récupère la configuration actuelle du port SSH
  if [[ $ssh_port_conf != "Port 2242" ]]; then                                  # S'il n'est pas égal à notre configuration désirée, on le change
    sed -i "s/$ssh_port_conf/Port 2242/" /etc/ssh/sshd_config;                  # On setup le port 2242 à la place de celui par défaut (22)
    echo "-> SSH port modified to 2242.";
    echo $separator;
  fi
}
