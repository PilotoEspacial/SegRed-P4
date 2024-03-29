#!/bin/bash


# Politicas por defecto
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Ping
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

# SSH
iptables -A INPUT -p tcp --dport 22 -s 10.0.1.3 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.2.0/24 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.3.0/24 -j ACCEPT

service ssh start
service rsyslog start

echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config

touch /var/log/auth.log

sed -i '/^DEBIAN_SNORT_INTERFACE/s//#&/' /etc/snort/snort.debian.conf
sed -i '/^DEBIAN_SNORT_HOME_NET/s//#&/' /etc/snort/snort.debian.conf

echo 'DEBIAN_SNORT_INTERFACE="eth0"' >> /etc/snort/snort.debian.conf
echo 'DEBIAN_SNORT_HOME_NET="10.0.3.0/24"' >> /etc/snort/snort.debian.conf

service ssh restart
service rsyslog restart
service fail2ban restart
service snort restart

ip route del default                                                                              
ip route add default via 10.0.3.2 dev eth0 

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
