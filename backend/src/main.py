import uvicorn

from core.config import api_settings, common_settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=api_settings.API_PORT,
        reload=common_settings.ENV_STAGE != "prod",
    )
