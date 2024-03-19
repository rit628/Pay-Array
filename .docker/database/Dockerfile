FROM mysql:8.3.0

COPY ./database/init.sql /docker-entrypoint-initdb.d/

ARG DATABASE_NAME_TEST
ARG DATABASE_NAME_PRODUCTION

RUN echo -e "CREATE DATABASE ${DATABASE_NAME_TEST};\nCREATE DATABASE ${DATABASE_NAME_PRODUCTION};\nUSE ${DATABASE_NAME_PRODUCTION};\n\n$(cat /docker-entrypoint-initdb.d/init.sql)" > /docker-entrypoint-initdb.d/init.sql