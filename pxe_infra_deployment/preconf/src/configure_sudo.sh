#!/bin/bash

function configure_sudo() {                                                     # On ajoute l'utilisateur créé aux sudoers
  check_sudo;
  local sample_root=$(cat /etc/sudoers | grep -e "root"$'\t' );
  local new_sudo="$username\tALL=(ALL:ALL) ALL";

  cat /etc/sudoers | grep -e "$new_sudo" >> /dev/null;                          # On teste si l'utilisateur est déjà dans les sudoers

  if [[ $? -ne 0 ]]; then                                                       # S'il n'y est pas présent, on l'ajoute
    echo "-> Now adding $username to sudoers.";
    sed -i "s/$sample_root/$sample_root\n$new_sudo/" /etc/sudoers;
    echo "-> $username added to sudoers.";
    echo $separator;
  fi
}

function check_sudo() {
  if ! command -v sudo &> /dev/null
  then
      echo "WARNING : sudo is not installed."
      echo -e "\tRunning apt install sudo :"
      apt install sudo;
  fi
}
