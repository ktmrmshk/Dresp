FROM python:3.6-slim
COPY requirements.txt .
RUN  apt update && apt install -y git \
     && apt clean && rm -rf /var/lib/apt/lists/* \
     && pip3 install -r requirements.txt \
     && rm -rf /root/.cache \
     && git clone https://github.com/ktmrmshk/Dresp.git 

ENV PYTHONPATH /Dresp/dresp
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000","drespweb:app"]


