#!/bin/bash

# Déclaration ici de plusieurs éléments graphiques pour l'UI

separator="#-   -   -   -   -   -   -   -   -   -#";

function end_configuration_interact() {                                                  # Fonction pour reboot la machine une fois toutes les modifications effectuées.
  echo -e "\n\n";
  echo "-> First setup is now completed."
  read -p "-> You must now reboot your machine. Would you like to do it now ? [Y/n] " confirmation;

  if [[ $confirmation == 'y' || $confirmation == 'Y' ]]; then
    echo "WARNING : Rebooting $new_hostname. Please wait..."
    /sbin/reboot;
  fi
}

function end_configuration() {                                                            # Fonction pour reboot la machine une fois toutes les modifications effectuées et supprimer les traces.
  local path_del=$(find / -name "preconf");
  echo -e "\n\n";
  echo "-> Pre-configuration is now completed.";
  echo;
  echo "-> Cleaning $path_del";
  rm -rf $path_del;
  echo "WARNING : Rebooting $new_hostname in 5 seconds. Please wait...";
  sleep 5;
  /sbin/reboot;
}

function start_configuration() {
  echo;
  echo "########################################";
  echo "#                                      #";
  echo "#       First Configuration for        #";
  echo "#            Customers VMs.            #";
  echo "#                                      #";
  echo "#      Please refer to README.md       #";
  echo "#        for more instructions.        #";
  echo "#                                      #";
  echo "#        Program provided by V.        #";
  echo "#                                      #";
  echo "########################################";
  echo;
}
