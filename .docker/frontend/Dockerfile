FROM node:20.11.0-bookworm

ARG WORKDIR

WORKDIR ${WORKDIR}

COPY ./frontend/package.json ./frontend/package-lock.jso[n] ./frontend/pnpm-lock.yam[l] ./frontend/yarn.loc[k] ./

RUN <<EOF
apt update
apt upgrade -y
npm install -g pnpm
pnpm install
EOF