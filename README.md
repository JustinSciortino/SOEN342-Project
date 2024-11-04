# SOEN342-Project Team 14
SOEN 342 Project

Justin Sciortino 40247931

Vito Rizzuto 40246408

All sequence diagrams, system sequence diagrams, operation contracts, domain model, package diagram and class diagram are in the Iterations_2 folder. Moving onwards, any updated/refined diagrams will be placed in the Iterations_2 folder even after the deadline of iteration 2. 

## Running the program instructions
To run main.py

1. Go to ```code``` directory
2. Install all dependencies by entering ```pipenv install```
3. Activate the pipenv by entering ```pipenv shell``` in the terminal
4. Run main.py by entering ```python main.py```

## Resetting the PostgreSQL DB Docker Image

1. Go to ```code``` directory
2. Stop the docker image by entering ```dcocker-compose down```
3. Show the volume to be deleted by entering ```docker volume ls```
4. Remove the volume named ```code_postgres_data``` by entering ```docker volume rm code_postgres_data```
5. Rebuild by doing ```docker-compose up --build -d```

## View DB information in terminal (Commands)
1. ```docker exec -it code-db-1 psql -U user -d lesson_management```
2. ```\l``` to view all databases
3. ```\c lesson_management``` to connect to the database
4. ```\dt``` to see the database tables
5. ```select * from tableName;``` or any other SQL command

