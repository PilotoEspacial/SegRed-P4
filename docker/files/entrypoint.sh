#!/bin/bash

service ssh start

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
