from db.base import DBSession
from db.models import Employee


class Statuses:
    active = 'active'
    hangover = 'hangover'
    vacation = 'vacation'


class StatusGroup:
    inactive = 'inactive'


class DFilter():
    conds = []

    def __init__(self, status: str) -> None:
        if status == StatusGroup.inactive:
            self.conds = [
                Employee.status.in_([Statuses.hangover, Statuses.vacation])
            ]

        super().__init__()


def dynamic_filter(session: DBSession, filter: DFilter = None):

    query = session.query(Employee)

    if filter is not None:
        query = query.filter(*filter.conds)

    employees = query.all()

    return employees
