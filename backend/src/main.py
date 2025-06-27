import argparse
import uvicorn
from dotenv import find_dotenv, load_dotenv


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the backend server.

    Returns:
        An argparse.Namespace object containing the parsed arguments.
    """
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


def load_environment(env: str) -> None:
    """Load environment variables, prioritizing environment-specific settings.

    Args:
        env: The environment string (e.g., "dev", "stage", "prod") to load
             the specific environment file for.
    """
    general_env_path = find_dotenv(".env")
    if general_env_path:
        load_dotenv(dotenv_path=general_env_path)
        print(f"Loaded general environment variables from: {general_env_path}")
    else:
        print(f"General .env file not found.")

    env_specific_path = find_dotenv(f".env.{env}")
    if env_specific_path:
        load_dotenv(dotenv_path=env_specific_path, override=False)
        print(f"Loaded environment-specific variables from: {env_specific_path}")
    else:
        print(f"Environment-specific .env file not found.")


def run_api() -> None:
    """Runs the FastAPI server using Uvicorn."""

    from core.config import api_settings, common_settings
    from core.logging import logger

    host = "0.0.0.0"
    port = api_settings.SERVER_API_PORT
    reload = common_settings.ENV_STAGE != "prod"

    logger.info(f"Starting server at http://{host}:{port} with reload={reload}")
    uvicorn.run("app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    args = parse_arguments()
    load_environment(args.ENV)
    run_api()
