FastApi Tasks Project

##Technologies: <br>
-Python 3.9.10
-FastAPI 0.71.0
-Postgresql 12

##Installation

-git clone https://github.com/RoofBite/FastApiTasks.git
-cd FastApiTasks

**How to run project with docker-compose:<br>**
-Rename .env_example file to .env
##Go to project root directory and run command:
-make run-app
- Go to http://0.0.0.0:8000/docs in browser

**To run test:<br>**
When app is running run in terminal:<br>
-docker ps <br>

Copy CONTAINER ID for IMAGE: fastapitasks_app<br>
Run in teminal command:<br>
-docker exec -it {CONTAINER ID} /bin/sh        #Example -> docker exec -it e26313fcd1c7 /bin/sh. <br>
Write in terminal:
-pytest



