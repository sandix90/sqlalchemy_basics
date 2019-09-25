from db.base import DBSession
from db.models import Employee


def get_one_employee(session: DBSession, eid: int) -> Employee:
    employee = session.query(Employee).filter(Employee.id == eid).one()

    print(f"ID: {employee.id}, {employee.first_name} {employee.last_name}")

    return employee
