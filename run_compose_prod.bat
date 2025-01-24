REM Build and run docker compose
docker compose -f compose.yml -f compose.prod.yml up --build -d

REM Keep the window open to view logs (optional)
pause

REM Stop and remove docker compose
docker compose -f compose.yml -f compose.prod.yml down