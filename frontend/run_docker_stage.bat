REM Build the Docker image 
docker build --target=stage -t cai-server-app-stage .

REM Run the Docker container
docker run -d -p 3000:3000 --env-file ../.env --name cai-server-app-stage-container cai-server-app-stage

REM Keep the window open to view logs (optional)
pause

REM Stop the Docker container
docker stop cai-server-app-stage-container