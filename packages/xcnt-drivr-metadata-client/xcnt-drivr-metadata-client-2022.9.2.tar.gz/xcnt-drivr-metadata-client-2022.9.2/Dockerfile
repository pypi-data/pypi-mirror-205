# Auto-generated from https://github.com/xcnt/xcnt-gardener/blob/main/templates/library/Dockerfile

FROM python:3.10-slim

LABEL MAINTAINER="XCNT GmbH <dev-infra@xcnt.io>"

ARG PIP_USERNAME
ARG PIP_PASSWORD
ARG PIP_EXTRA_INDEX_URL="https://${PIP_USERNAME}:${PIP_PASSWORD}@repository-manager.dev.xcnt.io/repository/pypi/simple"

WORKDIR /opt/app
ENV HOME /root

RUN addgroup --gid 9000 drivr && \
useradd -rm -d /opt/app -s /bin/bash -g drivr -u 9000 drivr && \
apt update && apt upgrade -y && \
apt install -y gcc libuuid1 postgresql-client && \
apt clean -y

ADD setup.py /opt/app

RUN apt update && apt install -y build-essential libpq-dev uuid-dev && \
pip install -U pip 'cython>=0.29.33' && \
pip install -e ".[test]" && \
pip uninstall -y cython && \
apt remove -y build-essential libpq-dev uuid-dev && \
apt autoremove -y && \
apt clean

ENV PYTHONPATH /opt/app

ADD . /opt/app

RUN python setup.py develop
