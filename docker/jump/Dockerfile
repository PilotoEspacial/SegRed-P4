FROM debian-base

RUN useradd -ms /bin/false jump && \
    mkdir /home/jump/.ssh && \
    chmod 700 /home/jump/.ssh

COPY assets/authorized_keys /home/jump/.ssh/authorized_keys

RUN chown jump:jump -R /home/jump

RUN chmod 644 /home/jump/.ssh/authorized_keys

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
