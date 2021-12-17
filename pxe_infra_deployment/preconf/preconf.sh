#!/bin/bash

source src/sources_includer.sh              # Ajout de toutes nos fonctions

root_test;
start_configuration;
echo $separator;
hostname_mod;
pimp_my_prompt;
root_passwd_modifier;
user_creator;
static_iface;
motd_modifier;
add_ssh_key;
no_ssh_root;
ssh_port_modifier;
configure_sudo;
tools_installation;
fail2ban_conf;

end_configuration;
