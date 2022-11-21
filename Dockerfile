FROM debian

RUN apt-get update && \
    apt-get install -y \
            iptables iproute2 net-tools tcpdump iputils-ping \
            curl netcat openssh-server

RUN useradd -ms /bin/bash dev && echo "dev:dev" | chpasswd

CMD service ssh start && /bin/bash
