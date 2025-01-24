REM Build the Docker image 
docker build --target=dev -t cai-server-api-dev .

REM Run the Docker container
docker run -d -p 5000:5000 --env-file ../.env --name cai-server-api-dev-container cai-server-api-dev

REM Keep the window open to view logs (optional)
pause

REM Stop the Docker container
docker stop cai-server-api-dev-container