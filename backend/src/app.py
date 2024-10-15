import os
import sys


sys.path.append("./")

from apis.base import api_router
from apis.utils.directory import dire
from core.config import settings
from db.base import Base
from db.session import engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_folders():
    if not os.path.exists(dire.image_path):
        os.makedirs(dire.image_path)
    if not os.path.exists(dire.conf_path):
        os.makedirs(dire.conf_path)
    for i in ["json", "model"]:
        if not os.path.exists(os.path.join(dire.conf_path, i)):
            os.makedirs(os.path.join(dire.conf_path, i))


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
    app.include_router(api_router)


def configure_staticfiles(app):
    app.mount(
        "/data",
        StaticFiles(directory=dire.data_path),
        name="data",
    )


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
    configure_staticfiles(app)
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg": "Hello Fast_API🚀"}
