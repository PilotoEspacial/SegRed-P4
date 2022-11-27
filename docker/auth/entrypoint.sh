#!/bin/bash

service ssh start
service rsyslog start

python3 auth.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
