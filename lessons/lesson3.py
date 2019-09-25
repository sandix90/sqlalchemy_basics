from sqlalchemy import func
from sqlalchemy.sql import exists

from db.base import DBSession
from db.models import Department


def get_departments_count(session: DBSession) -> int:
    count = session.query(Department).count()
    return count


def get_departments_func_count(session: DBSession) -> int:
    count = session.query(func.count(Department.id)).scalar()

    return count


def check_department_exists(session: DBSession, department_name: str) -> bool:

    is_exists = session.query(exists().where(Department.name == department_name)).scalar()

    return is_exists
