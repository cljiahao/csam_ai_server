import uvicorn

from core.config import api_settings, common_settings
from core.logging import logger

if __name__ == "__main__":
    host = "0.0.0.0"
    port = (
        api_settings.API_PORT
        if common_settings.ENV_STAGE == "prod"
        else api_settings.DEV_API_PORT
    )
    reload = common_settings.ENV_STAGE != "prod"

    logger.info(f"Starting server at http://{host}:{port} with reload={reload}")

    uvicorn.run("app:app", host=host, port=port, reload=reload)
