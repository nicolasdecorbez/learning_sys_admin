#!/bin/bash

function user_creator() { # Création d'un nouvel utilisateur en 3 étapes.
  echo "-> Creation of the user client"
  # get_username;                                                                   -> Si on veut une création intéractive de l'utilisateur
  # get_password;
  username=$(cat src/conf.d/user.conf | grep -e "USERNAME" | cut -d "=" -f 2);      # On lit dans le fichier user.conf les informations de user
  password=$(cat src/conf.d/user.conf | grep -e "PASSWORD" | cut -d "=" -f 2);
  create_user;
  echo $separator;
}

function get_username() {                                 # Récupère les information du nom de l'utilisateur.   ----------------------NON-UTILISÉE----------------------
  read -p "Enter the name of the new user : " username;
  local user_exists=$(getent passwd $username | cut -d ":" -f 1);

  while [[ $user_exists == $username ]]; do               # S'il est déjà prit, on bouce jusqu'au succès.
    echo "WARNING : Username already exist. Please try again : ";
    read -p "Enter the name of the new user : " username;
    user_exists=$(getent passwd $username | cut -d ":" -f 1);
  done
}

function get_password() {
  read -s -p "Enter the new password : " password;        # Entrée du mot de passe.                             ----------------------NON-UTILISÉE----------------------
  echo;
  read -s -p "Re-type the password : " password_check;    # Vérification du mot de passe.
  echo;

  while [[ $password != $password_check ]]; do            # Si les password ne correspondent pas, on recommence jusqu'à la réussite.
    echo -e "\nSorry, password do not match. Please try again : ";
    read -s -p "Enter the new password : " password;
    echo;
    read -s -p "Re-type the password : " password_check;
    echo;
  done
}

function create_user() {                                   # Une fois toutes les informations récupérées, on crée notre utilisateur.
  /sbin/useradd -s "/bin/bash" -m "$username";
  echo "$username:$password" | /sbin/chpasswd;                   # On ajoute le mot de passe.

  echo "-> User $username created."
}
