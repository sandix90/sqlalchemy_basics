from db.base import DBSession
from db.models import Department, CadreMovement
from db.models.employee import EmployeeWithCadreMovements


def has_in_relations(session: DBSession, reason: str):
    employees = session.query(EmployeeWithCadreMovements).filter(EmployeeWithCadreMovements.cadre_movements.any(CadreMovement.reason == reason)).all()
    return employees
