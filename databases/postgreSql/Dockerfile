FROM postgres:14


ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB


ENV POSTGRES_USER=tu_usuario
ENV POSTGRES_PASSWORD=tu_contraseña
ENV POSTGRES_DB=nombre_de_tu_base_de_datos

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
