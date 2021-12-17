#!/bin/bash

function root_test() {     # On teste si l'utilisateur qui lance le script est bien root, sinon on exit
  local who=$(whoami);
  if [[ $who != "root" ]]; then
    echo "WARNING : You must execute this script as root. Exiting the program.";
    exit;
  fi
}
