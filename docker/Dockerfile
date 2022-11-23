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
        && \
    apt-get clean

RUN useradd -ms /bin/bash op \
    && mkdir /home/op/.ssh

COPY assets/op.pub /home/op/.ssh/authorized_keys

RUN chown op:op -R /home/op \
    && chmod 700 -R /home/op/.ssh
