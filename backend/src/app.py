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

    if not os.path.exists(os.path.join(dire.data_path, "images")):
        os.makedirs(os.path.join(dire.data_path, "images"))
    app.mount(
        "/images",
        StaticFiles(directory=os.path.join(dire.data_path, "images")),
        name="images",
    )


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    configure_cors(app)
    include_router(app)
    configure_staticfiles(app)
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}
