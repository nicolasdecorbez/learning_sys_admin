#!/bin/bash

function tools_installation() {                                                 # Installation des outils nécessaires à la configuration
  echo "-> Checking required packages for configuration.";
  check_package2 "fail2ban";
  check_package "vim";
  check_package "rsync";
  check_package "wget";
  echo "-> All tools are installed.";
  echo $separator;
}

function check_package() {                                                      # On check si le package rentré en param est installé.
  if ! command -v $1 &> /dev/null
  then
      echo "WARNING : $1 is not installed."
      install_package "$1";
  fi
}

function check_package2() {                                                     # Test spécial pour fail2ban
  if ! command -v "$1-client" &> /dev/null
  then
      echo "WARNING : $1 is not installed."
      install_package "$1";
  fi
}

function install_package() {                                                    # Si le package n'est pas installé, on appelle cette fonction pour le faire
  echo -e "\tRunning apt install $1 :";
  apt -y install $1;
}
