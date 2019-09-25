from sqlalchemy import VARCHAR, Column, Text, ForeignKey

from db.models.base import BaseModel


class Skill(BaseModel):
    __tablename__ = 'skills'

    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text, nullable=True)


class EmployeesSkills(BaseModel):
    __tablename__ = 'employees_skills'

    employee_id = Column(ForeignKey('employees.id', ondelete='CASCADE'), nullable=False, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='CASCADE'), nullable=False, index=True)
