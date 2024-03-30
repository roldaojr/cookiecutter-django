FROM python:3.10-slim as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_PORT 8000
EXPOSE 8000
LABEL name="{{ cookiecutter.project_name }}"

ENV RUNTIME_DEPS="python3-pip"
ENV BUILD_DEPS="git python3-dev build-essential pkg-config"
ENV DEBUG="false"

RUN mkdir /app
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN apt-get update && apt install -y --no-install-recommends $RUNTIME_DEPS $BUILD_DEPS \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && pip3 install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install \
    && apt-get remove --purge -y $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base as app
COPY . /app/
CMD gunicorn

FROM app as app-with-static
RUN python manage.py collectstatic --ignore=*.scss --noinput
