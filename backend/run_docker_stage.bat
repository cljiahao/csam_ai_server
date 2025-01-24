REM Build the Docker image 
docker build --target=stage -t cai-server-api-stage .

REM Run the Docker container
docker run -d -p 8000:8000 --env-file ../.env --name cai-server-api-stage-container cai-server-api-stage

REM Keep the window open to view logs (optional)
pause

REM Stop the Docker container
docker stop cai-server-api-stage-container