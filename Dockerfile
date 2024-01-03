FROM python:3.10-slim AS base

LABEL maintainer="limeng.b@mininglamp.com"

COPY docker/sources.list /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash curl wget vim libmagic-dev \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir poetry \
    && poetry config virtualenvs.create false

COPY poetry.lock /env/poetry.lock
COPY pyproject.toml /env/pyproject.toml

RUN cd /env && poetry install --no-dev

EXPOSE 8086

WORKDIR /app

COPY . /app

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
