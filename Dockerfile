#From ktmrmshk/py3:latest
#RUN pip3 install setuptools \
#      && pip3 install flask \
#      && git clone https://github.com/ktmrmshk/Dresp.git  \
#      && cp /Dresp/dresp/drespstart.sh / \
#      && chmod +x /drespstart.sh

FROM python:3.6
RUN apt update && apt install -y --no-install-recommends git \
#      python3 python3-pip \
#      curl git \
      && apt clean \    
      && rm -rf /var/lib/apt/lists/* \
      && git clone https://github.com/ktmrmshk/kita_snippet.git \
      && pip3 install setuptools flask Pillow uwsgi \
      && git clone https://github.com/ktmrmshk/Dresp.git  
#      && cp /Dresp/dresp/drespstart.sh / \
#      && chmod +x /drespstart.sh

ENV PYTHONPATH /Dresp/dresp
EXPOSE 5000

CMD ["uwsgi", "--http", ":5000", "--wsgi-file", "/Dresp/dresp/drespweb.py", "--callable", "app"]
