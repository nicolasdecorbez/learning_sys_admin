#!/bin/bash

source src/pimp_my_script.sh;       # Outils d'affichage pour embélirle l'UI
source src/root_test.sh;            # Test si nous sommes bien l'utilisateur ROOT
source src/hostname_modifier.sh     # Changement du hostname
source src/pimp_my_prompt.sh        # Changement du prompt : user-host [~] -> $
source src/root_passwd_modifier.sh  # Changement du mot de passe root
source src/user_creator.sh          # Création d'un nouvel utilisateur
source src/static_iface.sh          # Modification de l'interface en static
source src/motd_modifier.sh         # Modification du MOTD
source src/add_ssh_key.sh           # Ajout d'une clé SSH pour une administration centralisée
source src/no_ssh_root.sh           # Désactivation du SSH en tant que root
source src/ssh_port_modifier.sh     # Modification du port SSH
source src/configure_sudo.sh        # Configuration de sudo pour le nouvel utilisateur
source src/tools_installation.sh    # Installation de différents packages dont nous aurons besoin
source src/fail2ban_conf.sh         # Configuration de fail2ban
