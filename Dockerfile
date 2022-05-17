FROM postgres:14.2
ENV POSTGRES_USER saiks2022
ENV POSTGRES_PASSWORD saiks2022
ENV POSTGRES_DB football
COPY create.sql /docker-entrypoint-initdb.d/
#COPY scripts/environment.yml /docker-entrypoint-initdb.d/
#COPY scripts/import_data.py /docker-entrypoint-initdb.d/
#COPY scripts/import_data.sh /docker-entrypoint-initdb.d/
#RUN cd /home && mkdir saiks
#RUN pg_createcluster 14 main
#RUN /etc/init.d/postgresql start 
#RUN --name saiks_postgres -e POSTGRES_PASSWORD=saiks2022 -p 5432:5432 -d saiks2022
#RUN psql -f /home/saiks/create.sql  
#RUN /etc/init.d/postgresql stop
#FROM continuumio/anaconda3:2020.11
#RUN cd /docker-entrypoint-initdb.d/ && conda remove --name saiks --all && conda env create && conda init bash 
#RUN conda activate saiks && python import_data.py


