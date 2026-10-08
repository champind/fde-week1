from fastapi import APIRouter
from data_store import employees

router = APIRouter()


@router.get("/employees")
def get_employees():
    return employees