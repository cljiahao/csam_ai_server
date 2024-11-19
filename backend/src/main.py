import uvicorn
import argparse
from dotenv import find_dotenv, load_dotenv


def load_environment(env):
    """Load environment variables from .env files based on the environment."""
    load_dotenv(dotenv_path=find_dotenv(".env.common"))
    load_dotenv(dotenv_path=find_dotenv(f".env.{env}"))


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="FastAPI Backend Server",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-e",
        "--ENV",
        help="Environment for dev, stage, prod.",
        type=str,
        choices=["dev", "stage", "prod"],
        default="dev",
    )
    return parser.parse_args()


def run_api():
    """Run the FastAPI server."""

    from core.config import api_settings, common_settings
    from core.logging import logger

    host = "0.0.0.0"
    port = api_settings.API_PORT
    reload = common_settings.ENV_STAGE != "prod"

    logger.info(f"Starting server at http://{host}:{port} with reload={reload}")
    uvicorn.run("app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    args = parse_arguments()
    load_environment(args.ENV)
    run_api()
