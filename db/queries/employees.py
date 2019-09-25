from ..base import DBSession
from db.models import Employee, EmployeeWithDepartments


def get_employee_id(session: DBSession, eid: int):
    employee = session.query(Employee).filter(Employee.id == eid).one()

    return employee


def get_employee_with_departments_by_id(session: DBSession, eid: int):
    employee = session.query(EmployeeWithDepartments).filter(Employee.id == eid).one()
    return employee