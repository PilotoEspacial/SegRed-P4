FROM debian-base


RUN apt-get update && \
    apt-get install -y \
        python \
        pip \
        && \
    apt-get clean

RUN pip install Flask Flask-RESTful requests

COPY broker.py broker.py
COPY cert /cert

RUN chmod 744 broker.py && \
    chmod -R 644 cert

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
