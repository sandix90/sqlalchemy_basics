from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import DBSession
from lessons.lesson1 import get_one_employee, get_employee_by_name
from lessons.lesson2 import get_all_departments
from lessons.lesson3 import check_department_exists, get_departments_count, get_departments_func_count
from lessons.lesson4 import dynamic_filter, DFilter, StatusGroup
from lessons.lesson5 import get_employee_with_skills
from lessons.lesson6 import has_in_relations
from lessons.lesson7 import aggragate_func_in_relatioship


import config

engine = create_engine(
        f'postgresql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}',
        pool_pre_ping=True
    )
session_factory = sessionmaker(bind=engine)
db_session = DBSession(session_factory())


def lesson_separation():
    print('_'*5)


tony_stark = get_employee_by_name(db_session, first_name='Tony', last_name='Stark')


print('Lesson 1: get employee by id')
get_one_employee(db_session, tony_stark.id)
lesson_separation()

print('Lesson 2: get all departments')
get_all_departments(db_session)
lesson_separation()

print('Lesson 3: count')

count = get_departments_count(db_session)
print(f'count: {count}')
count_func_result = get_departments_func_count(db_session)
print(f'count_func_result: {count_func_result}')

exists = check_department_exists(db_session, 'Legions')
print(f'Exists Legions: {exists}')
lesson_separation()

print('Lession 4: dynamic_filters')
dfilter = DFilter(status=StatusGroup.inactive)
inactive_heros = dynamic_filter(db_session, filter=dfilter)
print('Inactive_heros:')
for hero in inactive_heros:
    print(f'    Name: {hero}')

lesson_separation()


print('Lession 5: many-to-many')

employees_with_skills = get_employee_with_skills(session=db_session, eid=tony_stark.id)
for e in employees_with_skills:
    print(f'Employee {e} has skills:')
    for skill in e.skills:
        print(f'    Skill: {skill.name}, desc: {skill.description}')
lesson_separation()

print(f'Lession 6: Has in relations:')
employees = has_in_relations(db_session, 'simple')
for e in employees:
    print(f'    {e.first_name}: {e.last_name}')
lesson_separation()

print(f'Lession 7: aggregations in relationship')
employee = aggragate_func_in_relatioship(db_session, uid=tony_stark.id)
print(employee)


