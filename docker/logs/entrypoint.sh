#!/bin/bash

# Politicas por defecto
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Ping
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

service ssh start
service rsyslog start

# SSH config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config

# Rsyslog config
rm /etc/rsyslog.d/20-forward-logs.conf
rm /etc/rsyslog.d/50-sshd.conf

sed -i '/module(load="imudp")/s/^#//g' /etc/rsyslog.conf
sed -i '/input(type="imudp" port="514")/s/^#//g' /etc/rsyslog.conf

mkdir -p /var/log/remotelogs/
chown -R root:adm /var/log/remotelogs

service rsyslog restart

touch /var/log/auth.log

sed -i 's/logpath = \/var\/log\/auth.log/logpath = \/var\/log\/remotelogs\/logs\/sshd.log/g' /etc/fail2ban/jail.d/defaults-debian.conf

service ssh restart
service rsyslog restart
service fail2ban restart

ip route del default
ip route add default via 10.0.3.2 dev eth0 

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
