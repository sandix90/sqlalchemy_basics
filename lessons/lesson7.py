from db.base import DBSession
from db.models import EmployeeWithSkills


def aggragate_func_in_relatioship(session: DBSession, uid: int):
    result = session.query(EmployeeWithSkills).filter(EmployeeWithSkills.id == uid).one()
    return result
