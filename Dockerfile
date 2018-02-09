FROM python:3

COPY . /root/app
WORKDIR /root/app

RUN pip install -r requirements.txt

CMD gunicorn run:api -b 0.0.0.0:8001 