FROM debian-base

RUN useradd -ms /bin/bash dev \
    && mkdir /home/dev/.ssh

COPY assets/dev.pub /home/dev/.ssh/authorized_keys

RUN chown dev:dev -R /home/dev \
    && chmod 700 -R /home/dev/.ssh \
    && chmod 644 /home/dev/.ssh/authorized_keys

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
