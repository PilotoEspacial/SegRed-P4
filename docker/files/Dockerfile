FROM debian-base

RUN apt-get update && \
    apt-get install -y \
        python \
        pip \
        && \
    apt-get clean

RUN pip install Flask Flask-RESTful requests

COPY files.py files.py

RUN chmod 744 files.py

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
