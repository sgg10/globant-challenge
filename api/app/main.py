from typing import Union

from fastapi import FastAPI
import pkg_resources

from app.database.check_health import check_database_health


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/packages")
def get_packages():
    packages = []
    for package in pkg_resources.working_set:
        packages.append(
            {"package_name": package.project_name, "version": package.version}
        )
    return packages


@app.get("/health")
def health():
    database_health, database_message = check_database_health()
    return {
        "database": {
            "status": "ok" if database_health else "error",
            "message": database_message,
        },
        "general_status": "ok" if all([database_health]) else "error",
    }
