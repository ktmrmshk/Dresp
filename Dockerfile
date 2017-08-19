#From ktmrmshk/py3:latest
#RUN pip3 install setuptools \
#      && pip3 install flask \
#      && git clone https://github.com/ktmrmshk/Dresp.git  \
#      && cp /Dresp/dresp/drespstart.sh / \
#      && chmod +x /drespstart.sh

FROM ubuntu:16.04
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip \
      curl screen vim wget git \
      && apt-get clean \    
      && rm -rf /var/lib/apt/lists/* \
      && git clone https://github.com/ktmrmshk/kita_snippet.git \
      && pip3 install setuptools \
      && pip3 install flask \
      && pip3 install Pillow \
      && git clone https://github.com/ktmrmshk/Dresp.git  \
      && cp /Dresp/dresp/drespstart.sh / \
      && chmod +x /drespstart.sh

EXPOSE 5000

#CMD ["/usr/bin/python3", "/Dresp/dresp/drespweb.py"]
