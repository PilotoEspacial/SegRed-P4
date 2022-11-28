#!/bin/bash

service ssh start
service rsyslog start

# SSH config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config

# Rsyslog config
rm /etc/rsyslog.d/20-forward-logs.conf
rm /etc/rsyslog.d/50-sshd.conf

sed -i '/module(load="imudp")/s/^#//g' /etc/rsyslog.conf
sed -i '/input(type="imudp" port="514")/s/^#//g' /etc/rsyslog.conf

mkdir -p /var/log/remotelogs/
chown -R root:adm /var/log/remotelogs

#rsyslogd -N1 -f /etc/rsyslog.conf
#rsyslogd -N1 -f /etc/rsyslog.d/50-remote-logs.conf

service rsyslog restart

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
