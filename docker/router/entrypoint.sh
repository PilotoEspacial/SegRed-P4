#!/bin/bash

service ssh start
service rsyslog start

echo "PermitRootLogin no" >> /etc/ssh/sshd_config

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
