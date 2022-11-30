#!/bin/bash

service ssh start
service rsyslog start

#ip route del default # eliminar al puerta de enlace
#ip route add default via 10.0.3.2 dev eth0 # añadir la nueva puerta de enlace que es el router

# SSH config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
touch /var/log/auth.log

service ssh restart
service rsyslog restart
service fail2ban restart

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
