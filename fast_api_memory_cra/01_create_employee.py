from fastapi import APIRouter
from data_store import employees
from models import Employee

router = APIRouter()


@router.post("/employees")
def create_employee(employee: Employee):
    employees.append(employee.model_dump())

    return {
        "message": "Employee created successfully",
        "employee": employee
    }