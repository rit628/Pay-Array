FROM python:3.12.1-slim-bookworm

ARG WORKDIR

WORKDIR ${WORKDIR}

COPY ./backend/requirements.txt .

RUN python3.12 -m pip install -r requirements.txt