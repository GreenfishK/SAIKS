FROM postgres:14.2
ENV POSTGRES_USER saiks2022
ENV POSTGRES_PASSWORD saiks2022
ENV POSTGRES_DB football
COPY create.sql /docker-entrypoint-initdb.d/
