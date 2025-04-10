FROM apache/airflow:latest

USER root

RUN apt-get update &\
apt-get clean

USER airflow

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

