# SAIKS
A repository for the SAIKS lecture at the Vienna University of Technology. It contains the assignment data for the football ontology by group 11.

# Reproduce experiment
* Download Ontop plugin from [here](https://sourceforge.net/projects/ontop4obda/) or take the one from {SAIKS}/Protege/plugins/it.unibz.inf.ontop.protege-4.2.1.jar and copy it into your local protege/plugins folder. E.g. on linux: /opt/Protege/Protege-5.5.0/plugins
* Go into the root folder of this project and run: ```docker-compose up```. This will start a postgres database, create a database schema from the create.sql script and load data from the ./Datasets directory into the newly created schema. It will also start a web interface service for browsing the postgres database. This is only needed if you want to explore the database with a handy web tool (see Details below)
Now you are able to execute R2RML mappings and thereby transform relational data from the postgres databse to triples. To do this, start your local copy of Protege and execute following steps:
    * Load JDBC driver: Start Protege 5.5 and go to File > Preferences > JDBC Drivers > Add
        * Description: postgres
        * Class name: org.postgresql.Driver
        * Driver jar: {SAIKS}/Protege/jdbc_driver/postgresql-42.3.5.jar
    * Load the ontology: Open > {SAIKS}/Workspace/saiks2022ss_football_desktop.owl. This will also load the saiks2022ss_football_desktop.properties and the saiks2022ss_football_desktop.obda file from the same directory. The former file defines the jdbc connection string to the football schema of the postgres database. The latter file includes the ontop mappings.
    * Show Ontop mappings tab: Window > Tabs > Ontop Mappings
    * Select the Ontop Mappings tab and make sure that the connection parameters are populated (from the saiks2022ss_football_desktop.properties file). 
    * Test the connection: You should receive: Connection is ok
    * Select and run the ontop reasoner: Select Reasoner > Ontop 4.2.1 and then Reasoner > Start reasoner
    * Materialize triples: Go to Ontop > Materialize triples... : The mappings defined in saiks2022ss_football_desktop.obda, which are also visible in the Mapping manager tab within the Ontop Mappings tab, will be executed.

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
    
