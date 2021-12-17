#!/bin/bash

function root_passwd_modifier_old() {                         # Changement du mot de passe root                 ----------------------NON-UTILISÉE----------------------
  echo -e "You will now modify the root password. Please follow the instructions : ";
  passwd root;

  while [[ $? -ne 0 ]]; do                                # Si la modification échoue, on recommence jusqu'à la réussite.
    echo -e "\nModification of the root password failed. Please try again : ";
    passwd root;
  done

  echo -e "\n-> Root password changed.";
  echo $separator;
}

function root_passwd_modifier() {                                                         # Changement du mot de passe root.
  echo "-> Modification of the root password."
  root_passwd=$(cat src/conf.d/root.conf | grep -e "ROOT_PASSWORD" | cut -d "=" -f 2);    # On lit dans le fichier root.conf les informations de root
  echo "root:$root_passwd" | /sbin/chpasswd;                                                 # On applique la modification.
  echo "-> Root password changed.";
  echo $separator;
}
