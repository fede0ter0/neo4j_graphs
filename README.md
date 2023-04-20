# Data Engineering Coding Challenge

To solve this challenge, I have followed these steps:

- I'm using an Airflow Docker image. I made few changes in the `docker-compose.yaml`, in order to install additional requirements and add some folders.
- I'm using the Neo4j Docker image suggested in the neo4j documentation. 
- I worked based on the suggested model of proteins.
- I created a json dictionary in the path `schemas/docker-compose.yaml`. Its structure lets us parse the xml file, getting the nodes and relationships.
At the moment, I only coded the functions to parse and write the nodes, but the ones that write the relationships of the graph would be similar.
- For now, I tried to be pragmatic, so I didn't focus on a high quality design of the code (i.e., I didn't write different classes, I just put everything
into one single file).
- For tackling the problem, I thought about different solutions, and finally I tried to implement the fastest one.

## Steps for running the script:

- Inside the root folder, run `docker run --publish=7474:7474 --publish=7687:7687 --volume=$PWD/neo4j/data:/data --env=NEO4J_AUTH=none neo4j` to start
the Neo4j instance.
- Build the Airflow docker with `docker compose build`. After that, start the docker compose with `docker compose up`.
- Airflow webserver will be available at `http://localhost:8080/home`. Also, Neo4j service interface will be at `http://localhost:7474`.
- In the Airflow UI, it should appear the DAG `dag_uniprot`. It can be ran manually, and should take some seconds to finish. After that, you can get into the 
Neo4j browser and type `MATCH (n) RETURN n;`. That will show every graph in the database. You should see two different types of nodes: `proteins` and `genes`.
That is what I have implemented for now.
