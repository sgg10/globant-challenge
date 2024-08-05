from typing import Union

from fastapi import FastAPI
import pkg_resources

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
