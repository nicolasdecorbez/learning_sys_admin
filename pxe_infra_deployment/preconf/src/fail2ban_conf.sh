#!/bin/bash

function fail2ban_conf() {
  echo "-> Configuration of fail2ban..."
  local default_deb="/etc/fail2ban/jail.d/defaults-debian.conf";
  cp -a src/fail2ban_jails/. /etc/fail2ban/jail.d/ ;                            # On ajoute nos nouvelles jails
  if [[ -f $default_deb ]]; then                                                # Si le fichier defaults-debian.conf existe, on fait un backup en .old
    mv "$default_deb" "$default_deb.old";
  fi

  systemctl restart fail2ban;                                                   # Puis on restart le service fail2ban
  echo "-> fail2ban is now running."
  echo $separator;
}
