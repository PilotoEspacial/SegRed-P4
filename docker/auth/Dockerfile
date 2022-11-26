FROM debian-base

RUN apt-get update && \
    apt-get install -y \
        python \
        pip \
        && \
    apt-get clean

RUN pip install Flask Flask-RESTful requests

COPY auth.py /auth.py
RUN chmod 744 auth.py

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
