#!/bin/bash

service ssh start
service rsyslog start

python3 broker.py

echo "PermitRootLogin no" >> /etc/ssh/sshd_config

touch /var/log/auth.log

service ssh restart
service rsyslog restart
service fail2ban restart

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
