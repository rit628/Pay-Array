FROM node:20.11.0-bookworm

ARG WORKDIR

WORKDIR ${WORKDIR}

COPY ./frontend/package.json ./frontend/package-lock.jso[n] ./frontend/pnpm-lock.yam[l] ./frontend/yarn.loc[k] ./

RUN apt-get update && \
apt-get upgrade -y && \
npm install -g pnpm && \
pnpm import && \
pnpm install