FastApi Tasks Project

## Technologies: <br>
-Python 3.9.10 <br>
-FastAPI 0.71.0 <br>
-Postgresql 12 <br>

## Installation <br>

    git clone https://github.com/RoofBite/FastApiTasks.git

    cd FastApiTasks

## How to run project with docker-compose:<br>
1: Rename .env_example file to .env <br>
2: **Go to project root directory and run command:** <br>

    make run-app

3: Go to http://0.0.0.0:8000/docs in browser <br>

## To run test:<br>
1: When app is running run in terminal:<br>

    docker exec -it fastapitasks_app_1 /bin/sh

#Example: <br>

       docker exec -it e26313fcd1c7 /bin/sh
2: Write in terminal: <br>

    pytest
