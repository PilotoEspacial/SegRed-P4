FROM debian-base

RUN apt-get update && \
    apt-get install -y \
        python \
        pip \
        && \
    apt-get clean

RUN pip install Flask Flask-RESTful pyjwt requests

COPY auth.py /auth.py
COPY certs /certs
COPY keys /keys


RUN chmod 744 auth.py && \
    chmod -R 644 certs && \
    chmod -R 644 keys


COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
