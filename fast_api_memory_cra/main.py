import importlib

from fastapi import FastAPI


create_employee = importlib.import_module("01_create_employee").router
get_employee = importlib.import_module("01_get_employee").router


app = FastAPI()


app.include_router(create_employee)
app.include_router(get_employee)