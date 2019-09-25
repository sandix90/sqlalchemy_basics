from sqlalchemy import Column, VARCHAR, ForeignKey, select, func, and_
from sqlalchemy.orm import relation, column_property

from .cadre_movements import CadreMovement
from db.models.department import EmployeeDepartments, Department
from db.models.skill import Skill, EmployeesSkills
from .base import BaseModel


class Employee(BaseModel):
    __tablename__ = 'employees'

    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    phone = Column(VARCHAR(255), unique=True, nullable=True)
    description = Column(VARCHAR(255), nullable=True)
    status = Column(VARCHAR(100), nullable=True)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class EmployeeWithSkills(Employee):
    skills = relation(Skill, secondary=EmployeesSkills.__tablename__, lazy='joined')

    skills_count = column_property(select([func.count(EmployeesSkills.id)]).where(EmployeesSkills.employee_id == Employee.id))
    last_cadre_movement = relation(
        CadreMovement,
        uselist=False,
        primaryjoin=and_(
            CadreMovement.employee == Employee.id,
            CadreMovement.id == select([func.max(CadreMovement.id)]).where(CadreMovement.employee == Employee.id)
        )
    )


class EmployeeWithCadreMovements(Employee):
    cadre_movements = relation('CadreMovement', uselist=True, foreign_keys='CadreMovement.employee')


class EmployeeWithDepartments(Employee):
    departments = relation(
        Department,
        # primaryjoin=EmployeeDepartments.employee_id == Employee.id,
        secondary=EmployeeDepartments.__tablename__,
        # secondaryjoin=EmployeeDepartments.department_id == Department.id,
        viewonly=True
    )
