FROM debian

RUN apt-get update && \
    apt-get install -y \
        iptables \
        iproute2 \
        net-tools \
        tcpdump \
        iputils-ping \
        nano \
        less \
        openssh-server \
        rsyslog \
        curl \
        sudo \
        fail2ban \
        && \
    apt-get clean

RUN useradd -ms /bin/bash op \
    && mkdir /home/op/.ssh \
    && chmod 700 -R /home/op/.ssh

COPY assets/ssh/op.pub /home/op/.ssh/authorized_keys

COPY assets/rsyslog/20-forward-logs.conf /etc/rsyslog.d/20-forward-logs.conf

COPY assets/rsyslog/50-sshd.conf /etc/rsyslog.d/50-sshd.conf

COPY assets/fail2ban/defaults-debian.conf /etc/fail2ban/jail.d/defaults-debian.conf

RUN chmod 644 /home/op/.ssh/authorized_keys && chown op:op -R /home/op
