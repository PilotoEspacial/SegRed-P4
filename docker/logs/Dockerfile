FROM debian-base

COPY entrypoint.sh /entrypoint.sh

COPY assets/50-remote-logs.conf /etc/rsyslog.d/50-remote-logs.conf

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
