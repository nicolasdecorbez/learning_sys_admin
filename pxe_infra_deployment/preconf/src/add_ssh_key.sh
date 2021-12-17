#!/bin/bash

function add_ssh_key() {
  local ssh_path="/home/$username/.ssh";                                        # On génère notre path de .ssh
  local akeys_path="$ssh_path/authorized_keys";                                 # On génère notre path de authorized_keys dans .ssh
  local new_ssh_key=$(cat src/ssh/id_rsa.pub);                                  # On récupère notre clé ssh

  if [[ ! -d $ssh_path ]]; then                                                 # On crée le dossier .ssh s'il n'existe pas
    mkdir $ssh_path;
  fi

  if [[ -f $akeys_path ]]; then                                                 # Si le fichier authorized_keys existe, on essaye de récupérer une clé portant le même nom que notre actuelle
    local old_ssh_key=$(cat $akeys_path | grep "admin_server");
    if [[ $? -ne 0 ]]; then
      cat src/ssh/id_rsa.pub >> $akeys_path;                                    # On ajoute notre clée à notre authorized_keys, sans modifier le fichier de base
      echo "-> SSH key added to $akeys_path";
      echo $separator;
    else
      sed -i "s/$old_ssh_key/$new_ssh_key/" $akeys_path;                        # S'il existe une clé SSH portant le même nom, on l'override avec notre nouvelle
      echo "-> SSH key added to $akeys_path";
      echo $separator;
    fi
  else
    cat src/ssh/id_rsa.pub > $akeys_path;                                       # On ajoute notre clée à notre authorized_keys, en créant le fichier
    echo "-> SSH key added to $akeys_path";
    echo $separator;
  fi
}
