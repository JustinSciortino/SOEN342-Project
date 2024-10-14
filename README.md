# SOEN342-Project Team 14
SOEN 342 Project

Justin Sciortino 40247931

Vito Rizzuto 40246408


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
5. Rebuild by doing ```docker-compose up --buid -d```
