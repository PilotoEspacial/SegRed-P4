#!/bin/bash


ip route de1 default
ip route add default via 10.0.2.2 dev eth0

service ssh start
service rsyslog start

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
