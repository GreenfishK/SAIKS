# SAIKS
A repository for the SAIKS lecture at the Vienna University of Technology. It contains the assignment data for the football ontology by group 11.

# Reproduce experiment
* Download Ontop plugin from [here](https://sourceforge.net/projects/ontop4obda/) and copy it into your local protege/plugins folder. \\
* Go into the root folder of this project and run: ```docker-compose up```. This will start a postgres database, create a database schema from the create.sql script and load data from the ./Datasets directory into the newly created schema.
* Now you are able to execute SPARQL queries on top of the postgres database with Protege.
