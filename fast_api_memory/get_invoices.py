from fastapi import FastAPI

app = FastAPI()

invoices = [
    {"id": 1, "vendor": "Vendor A", "amount": 50000, "status": "Paid"},
    {"id": 2, "vendor": "Vendor B", "amount": 150000, "status": "Pending"},
    {"id": 3, "vendor": "Vendor C", "amount": 75000, "status": "Paid"}
]

employees = [
    {"id": 1, "name": "John", "department": "IT"},
    {"id": 2, "name": "Smith", "department": "HR"},
    {"id": 3, "name": "David", "department": "Finance"}
]

@app.get("/invoices")
def get_invoices():
    return invoices

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return {"message": "Employee not found"}