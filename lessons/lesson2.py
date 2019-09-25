from typing import List

from db.base import DBSession
from db.models import Department


def get_all_departments(session: DBSession) -> List[Department]:
    departments = session.query(Department).all()

    for department in departments:
        print(f'ID: {department.id}, name: {department.name}')

    return departments
