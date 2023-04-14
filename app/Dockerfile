FROM python:3.8

ENV PYTHONIOENCODING utf-8

WORKDIR /app

RUN apt update
RUN apt install -y
RUN apt install -y python3-pip
RUN pip install --upgrade pip

COPY requirements.txt .

RUN python3.8 -m pip install -r requirements.txt

COPY ./app/src/ /app