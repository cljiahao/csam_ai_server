REM Build the Docker image 
docker build --target=dev -t cai-server-app-dev .

REM Run the Docker container
docker run -d -p 5173:5173 --env-file ../.env --name cai-server-app-dev-container cai-server-app-dev

REM Keep the window open to view logs (optional)
pause

REM Stop the Docker container
docker stop cai-server-app-dev-container