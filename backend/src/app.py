import os
import sys


sys.path.append("./")

from apis.routes import router
from core.directory import directory
from core.config import settings
from db.base import Base
from db.session import engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_folders():
    folders = [
        directory.log_dir,
        directory.json_dir,
        directory.model_dir,
        directory.images_dir,
        directory.data_send_dir,
    ]
    for fol in folders:
        if not os.path.exists(fol):
            os.makedirs(fol)


def configure_cors(app):
    origins = settings.CORS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_router(app):
    app.include_router(router)


# TODO: add metadatas (Tags,Summary,Description) to fastapi


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        root_path=settings.FASTAPI_ROOT,
    )
    create_tables()
    create_folders()
    configure_cors(app)
    include_router(app)

    return app


app = start_application()


@app.get("/")
def home():
    return {"msg": "Hello Fast_API🚀"}
