from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relation

from .department import Department
from .base import BaseModel


class CadreMovement(BaseModel):
    __tablename__ = 'cadre_movements'

    employee = Column(Integer, ForeignKey('employees.id', ondelete='CASCADE'), nullable=False, index=True)
    old_department = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'), nullable=False, index=True)
    new_department = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'), nullable=False, index=True)
    reason = Column(VARCHAR(500), nullable=True)

    department = relation(Department, foreign_keys=new_department, lazy='select')
