#!/bin/bash

function no_ssh_root() {
  ssh_root_conf=$(cat /etc/ssh/sshd_config | grep -e "#PermitRootLogin ");      # On récupère le statut actuel de notre configuration SSH pour root
  if [[ $? -eq 0 ]]; then                                                       # Si grep a réussi à trouver cette ligne avec un commentaire, alors on la modifie
    sed -i "s/$ssh_root_conf/PermitRootLogin no/" /etc/ssh/sshd_config;         # On bloque l'accès dans /etc/ssh/sshd_config
    echo "-> SSH connection to root disabled.";
    echo $separator;
  fi
}
