#!/bin/bash

python3 auth.py

# Politicas por defecto
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Ping
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

service ssh start
service rsyslog start

echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config

touch /var/log/auth.log

service ssh restart
service rsyslog restart
service fail2ban restart

ip route del default
ip route add default via 10.0.2.2 srv eth0

pip install -r requirements.txt
python3 auth.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
