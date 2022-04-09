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

    docker ps 

2: Copy CONTAINER ID for IMAGE: fastapitasks_app<br>
3: Run in teminal command:<br>
    
    docker exec -it {CONTAINER ID} /bin/sh 

#Example: <br>

       docker exec -it e26313fcd1c7 /bin/sh
4: Write in terminal: <br>

    pytest



