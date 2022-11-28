#!/bin/bash

service ssh start
service rsyslog start

python3 broker.py

echo "PermitRootLogin no" >> /etc/ssh/sshd_config

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
