from sqlalchemy import Column, VARCHAR, Integer, ForeignKey

from .base import BaseModel


class Department(BaseModel):
    __tablename__ = 'departments'

    name = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=False)


class EmployeeDepartments(BaseModel):
    __tablename__ = 'employee_departments'

    employee_id = Column(Integer, ForeignKey('employees.id', ondelete='CASCADE'), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'), nullable=False, index=True)
