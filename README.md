# SAIKS
A repository for the SAIKS lecture at the Vienna University of Technology. It contains the assignment data for the football ontology by group 11.

# Reproduce experiment
* Download Ontop plugin from [here](https://sourceforge.net/projects/ontop4obda/) and copy it into your local protege/plugins folder.
* Go into the root folder of this project and run: ```docker-compose up```. This will start a postgres database, create a database schema from the create.sql script and load data from the ./Datasets directory into the newly created schema. It will also start a web interface service vor browsing the postgres database. This is only needed if you want to explore the database with a handy web tool (see Details below)
* Now you are able to execute SPARQL queries on top of the postgres database with Protege.

## Explore database with pgadmin
* Open the browser and go to http://localhost:5555/browser/
* Provide following credentials and proceed: 
    * user: admin@developer-blog.net
    * pw: admin
* In the Dashboard view click on "Add New Server"
* Provide the following parameter values:
    * General/Name: saiks
    * Connection/Host name: saiks
    * Connection/Maintenance database: football
    * Connection/Username: saiks2022
    * Connection/Password: saiks2022
* Click Save

Now you can expand the database in the left side bar and navigate to the database tables: Server/saiks/Databases/football/Schemas/public/Tables. There you can right click on any table and click on "View/Edit Data > All Rows" to see all rows from that table.
    
