FROM postgres:latest
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=joanderson
ENV POSTGRES_PASSWORD=ifpb
COPY init.sql /docker-entrypoint-initdb.d/
