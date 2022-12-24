FROM debian-base


RUN apt-get update && \
    apt-get install -y \
        python \
        pip \
        && \
    apt-get clean

RUN pip install flask flask-restful pyjwt requests

COPY broker.py broker.py
COPY certs /certs
COPY keys /keys

RUN chmod 744 broker.py && \
    chmod -R 644 certs && \
    chmod -R 644 keys

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
