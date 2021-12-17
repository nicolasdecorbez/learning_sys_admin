#!/bin/bash

function pimp_my_prompt() {
  if [[ $USER == "root" && $SUDO_USER ]]; then                                    # Si la commande est lancée avec sudo
    local bashrc_path="/home/$SUDO_USER/.bashrc";
  else                                                              # Si la commande est lancée avec su
    local bashrc_path="/home/$USER/.bashrc";
  fi
  change_ps1 $bashrc_path;                                          # On change pour l'utilisateur actuel
  change_ps1 "/etc/skel/.bashrc";                                   # On change le skel pour les prochains utilisateurs
  change_ps1 "/root/.bashrc";                                       # On change également le prompt du root
}

function change_ps1() {
  local prompt_check=$(cat $1 | grep -e "export PS1");                    # Check si une ligne PS1 existe déjà

  if [[ $prompt_check != 'export PS1="\u-\H [\w] -> \$ "' ]]; then  # Si prompt_check n'est pas égal à notre prompt désiré
    echo 'export PS1="\u-\H [\w] -> \$ "' >> $1;
    echo "-> Prompt changed in $1.";
    echo $separator;
  fi
}
