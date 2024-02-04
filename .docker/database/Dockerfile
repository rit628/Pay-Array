FROM mysql:8.3.0

COPY ./database/init.sql /docker-entrypoint-initdb.d/

ARG DATABASE_NAME

RUN echo -e "CREATE DATABASE ${DATABASE_NAME};\nUSE ${DATABASE_NAME};\n\n$(cat /docker-entrypoint-initdb.d/init.sql)" > /docker-entrypoint-initdb.d/init.sql