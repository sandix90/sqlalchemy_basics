from db.base import DBSession
from db.models import Employee


def get_one_employee(session: DBSession, eid: int) -> Employee:
    employee = session.query(Employee).filter(Employee.id == eid).one()

    print(f"ID: {employee.id}, {employee.first_name} {employee.last_name}")

    return employee


def get_employee_by_name(session: DBSession, first_name: str, last_name: str) -> Employee:
    employee = session.query(Employee).filter(Employee.first_name == first_name, Employee.last_name == last_name).one()
    return employee
