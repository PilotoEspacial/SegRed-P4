#!/bin/bash

service ssh start
service rsyslog start

python3 files.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
