"""table data

Revision ID: 60b4rc26f1a7
Revises: 59a3f9bc7288
Create Date: 2019-10-06 14:56:07.564667

"""

from sqlalchemy import orm

from alembic import op
from db.models import Employee, Skill, Department, EmployeesSkills, CadreMovement, EmployeeDepartments

revision = '60b4rc26f1a7'
down_revision = '59a3f9bc7288'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Skills creation:

    fly_skill = Skill(name='Fly', description='I believe I can Fly. I believe I can touch the sky')
    light_shield_skill = Skill(name='Light Shield', description='Light protect. Perfect for everything')
    heavy_shield_skill = Skill(name='Heavy Shield', description='Try to hurt me')
    elbanador_skill = Skill(name='Elbanador ability', description='Godlike')
    flexibility_skill = Skill(name='Flexibility', description='Like a rubber')
    decrease_skill = Skill(name='Decrease', description='As less as it possible')

    session.add_all([fly_skill,  light_shield_skill, heavy_shield_skill, elbanador_skill, flexibility_skill, decrease_skill])
    session.flush()

    # Departmets creation:
    guards_department = Department(name='Guards', description='People, who protect us from UFO')
    legions_department = Department(name='Legions', description='Just Legions')
    session.add_all([guards_department, legions_department])
    session.flush()

    # Employees creation:
    tony_stark = Employee(first_name='Tony', last_name='Stark', phone='+52 111 111 11 11', description='Iron Man', status='vacation')
    steve_rogers = Employee(first_name='Steve', last_name='Rogers', phone='+52 222 222 22 22', description='Captain America', status='active')
    peter_parker = Employee(first_name='Peter', last_name='Parker', phone='+52 333 333 33 33', description='Spider Man', status='hangover')
    scott_lang = Employee(first_name='Scott', last_name='Lang', phone='+52 444 444 44 44', description='Ant Man', status='hangover')

    session.add_all([tony_stark, steve_rogers, peter_parker, scott_lang])
    session.flush()

    # Employees Skills
    session.add_all([
        EmployeesSkills(employee_id=tony_stark.id, skill_id=fly_skill.id),
        EmployeesSkills(employee_id=tony_stark.id, skill_id=light_shield_skill.id),
        EmployeesSkills(employee_id=tony_stark.id, skill_id=elbanador_skill.id),
        EmployeesSkills(employee_id=steve_rogers.id, skill_id=heavy_shield_skill.id),
        EmployeesSkills(employee_id=peter_parker.id, skill_id=flexibility_skill.id),
        EmployeesSkills(employee_id=scott_lang.id, skill_id=decrease_skill.id),
    ])

    # Employee CadreMovements
    session.add_all([
        CadreMovement(employee=tony_stark.id, old_department=guards_department.id, new_department=legions_department.id, reason='simple'),
        CadreMovement(employee=tony_stark.id, old_department=legions_department.id, new_department=guards_department.id, reason='simple'),
        CadreMovement(employee=steve_rogers.id, old_department=guards_department.id, new_department=legions_department.id, reason='simple'),
        CadreMovement(employee=peter_parker.id, old_department=legions_department.id, new_department=guards_department.id, reason='complicated'),
    ])

    # Employee departments
    session.add_all([
        EmployeeDepartments(employee_id=tony_stark.id, department_id=guards_department.id),
        EmployeeDepartments(employee_id=tony_stark.id, department_id=legions_department.id),
    ])

    session.commit()


def downgrade():
    pass