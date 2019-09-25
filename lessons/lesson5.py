from db.base import DBSession
from db.models import EmployeeWithSkills


def get_employee_with_skills(session: DBSession, eid: int):
    employee = session.query(EmployeeWithSkills).all()

    return employee
