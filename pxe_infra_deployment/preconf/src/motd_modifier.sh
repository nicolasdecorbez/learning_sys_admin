#!/bin/bash

function motd_prep() {
  rm -f /etc/update-motd.d/10-uname;                                                                                                  # On supprime le fichier MOTD dynamique
  if [[ $(cat /etc/pam.d/login | grep -e "pam_lastlog.so" | cut -c 1) != '#' ]]; then
    sed -i '/^session    optional   pam_lastlog.so/ s/./#&/' /etc/pam.d/login;                                                        # On supprime le message de login
  fi
  echo -e "Virtual machine provided by V. Please contact you administrator if you are encountering any problem."> /etc/motd;        # On modifie le fichier MOTD static en remplaçant le message par défaut
  echo "-> Old MOTD deleted. Now generating a new one."
}

function motd_creator() {
  cp -a src/new_motd/. /etc/update-motd.d/ ;                                                                                          # On copie nos nouveaux le fichier MOTD dynamique
  chmod +x /etc/update-motd.d/*;                                                                                                      # On accorde les droits d'execution à nos fichiers
  echo "-> New MOTD generated.";
}

function motd_modifier() {
  motd_prep;
  motd_creator;
  echo $separator;
}
