FROM debian-base


RUN apt-get install update && \
    apt-get install -y \
    python \
    pip && \

    apt-get clean

RUN pip install Flask ==1.1.2 Flask-RESTful==0.3.8 request



COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
