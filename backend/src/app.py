from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.routes import router
from core.config import common_settings, api_settings
from db.base import Base
from db.session import engine


def create_tables() -> None:
    """Create database tables based on the metadata."""
    Base.metadata.create_all(bind=engine)


def configure_cors(app: FastAPI) -> None:
    """Configure CORS settings for the FastAPI application."""
    origins = api_settings.ALLOWED_CORS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_router(app: FastAPI) -> None:
    """Include application routers."""
    app.include_router(router)


# TODO: add metadatas (Tags,Summary,Description) to fastapi


def start_application() -> FastAPI:
    """Initialize and configure the FastAPI application."""
    app = FastAPI(
        title=common_settings.PROJECT_NAME,
        version=common_settings.PROJECT_VERSION,
        description=common_settings.PROJECT_DESCRIPTION,
        root_path="/api",
    )

    configure_cors(app)
    include_router(app)
    create_tables()

    return app


# Initialize the FastAPI application
app = start_application()


@app.get(
    "/",
    tags=["Home"],
    summary="Home Route",
    description="A simple home route returning a welcome message.",
)
def home() -> dict[str, str]:
    """Simple home route."""
    return {"msg": "Hello Fast_API 🚀"}
