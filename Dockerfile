From ktmrmshk/py3:latest

RUN pip3 install setuptools \
      && pip3 install flask \
      && git clone https://github.com/ktmrmshk/Dresp.git  \
      && cp /Dresp/dresp/drespstart.sh / \
      && chmod +x /drespstart.sh

EXPOSE 5000

CMD ["/usr/bin/python3", "/Dresp/dresp/drespweb.py"]
