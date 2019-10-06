Доброго дня.
Сегодня хочу рассказать про ORM SQLAlchemy. Поговорим о том, что это, про его возможности и гибкость, а также рассмотрим случаи, которые не всегда понятно описаны.
Данная ORM имеет порог вхождения выше среднего, поэтому я попытаюсь объяснить всё простым языком и с примерами. Статья будет полезна тем, кто уже работает с sqlalchemy 
и хочет прокачать свои навыки или только знакомится с этой библиотекой.
<cut/>
Используемый язык программирования  —  python 3.6.
БД - PostgreSQL.
Ссылка на [github](https://github.com/sandix90/sqlalchemy_basics)


Итак, что такое ORM? 
ORM (Object-Relational Mapping)  —  это технология, которая позволяет сопоставлять модели, типы которых несовместимы. Например: таблица базы данных и объект языка программирования. 
Иными словами, можно обращаться к объектам классов для управления данными в таблицах БД. Также можно создавать, изменять, удалять, фильтровать и, самое главное, наследовать объекты классов, 
сопоставленные с таблицами БД, что существенно сокращает наполнение кодовой базы. 

Чтобы использовать возможности SQLAlchemy, необходимо понять принцип его работы.
Разработчикам, которые используют Django-ORM, придется немного перестроить образ мышления для создания ORM запросов. На мой взгляд, SQLAlchemy - функциональный монстр,
 возможностями которого можно и нужно пользоваться, но нужно понимать, что ORM не всегда идеальны. Поэтому обсудим моменты, когда использование этой технологии целесообразно.

В SQLAlchemy есть понятие декларативных и недекларативных определений моделей. Недекларативные определения подразумевают использования mapper(), 
описывающего сопоставление каждой колонки БД и классом модели. 
В данной статье используется декларативное определение моделей. 
Подробнее [здесь](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base)

### Структура БД
Для полной консистентности данных давайте создадим следующие таблицы.


Базовая модель служит для определения базовых колонок в БД.

    class BaseModel(Base):
        __abstract__ = True
    
        id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
        created_at = Column(TIMESTAMP, nullable=False)
        updated_at = Column(TIMESTAMP, nullable=False)
    
        def __repr__(self):
            return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

Employee - таблица, описывающая работника, который работает в офисе

    class Employee(BaseModel):
        __tablename__ = 'employees'
    
        first_name = Column(VARCHAR(255), nullable=False)
        last_name = Column(VARCHAR(255), nullable=False)
        phone = Column(VARCHAR(255), unique=True, nullable=True)
        description = Column(VARCHAR(255), nullable=True)
        
EmployeeWithSkills - не таблица. Класс наследуемый от Employee. Отличная возможность разделить логику и использовать класс, будто это отдельная таблица.

    class EmployeeWithSkills(Employee):
        skills = relation(Skill, secondary=EmployeesSkills.__tablename__, lazy='joined')
            
Department - отдел, в котором работает этот сотрудник. Человек может состоять в нескольких отделах.
    
    class Department(BaseModel):
        __tablename__ = 'departments'
    
        name = Column(VARCHAR(255), nullable=False)
        description = Column(VARCHAR(255), nullable=False)

Таблица соответствий работника и подразделений, в которых он состоит.

    class EmployeeDepartments(BaseModel):
        __tablename__ = 'employee_departments'
        
        employee_id = Column(Integer, ForeignKey('employees.id', ondelete='CASCADE'), nullable=False, index=True)
        department_id = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'), nullable=False, index=True)
        
Таблица соответствий сотрудников и их умений.
    
    class EmployeesSkills(BaseModel):
    __tablename__ = 'employees_skills'
    
    employee_id = Column(ForeignKey('employee.id', ondelete='CASCADE'), nullable=False, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='CASCADE'), nullable=False, index=True)

  
Создаем миграции с помощью пакета alembic, позволяющего генерировать их автоматически. В рамках данного урока автогенерация миграций вполне допустима.
В последней миграции присутствуют тестовые данные, которые наполнят базу.
Как настроить alembic можно почитать [здесь](https://alembic.sqlalchemy.org/en/latest/)
Выполняем заветные alembic upgrade head, чтобы выполнить миграцию.

### Запросы и relations
Давайте сделаем первый запрос и получим информацию о сотруднике по его id. 
Запрос будет выглядеть так:
    
lesson1:
  
    employee = session.query(Employee).filter(Employee.id == eid).one()
    
    output:
        ID: 2, Tony Stark

`.one()`  в конце обозначает, что мы намерены получить только одну запись. Если записей будет несколько, возникнет соответствующее исключение.

Если мы захотим получить все имеющиеся отделы, то можно воспользоваться следующим запросом c использованием `.all()`

lesson2:

    emmployee = session.query(Department).all()
    
    output:
        ID: 2, name: Guards
        ID: 4, name: Legions
        
Рассмотрим работу с функциями агрегации. 
Мы можем получить количество имеющихся департаментов с помощью встроенной функции
`.count()` или использовать `func.count()`. С помощью второго метода можно обращаться к любым функциям SQL, используя для `select` 
или для вычисления промежуточных результатов. 

lesson3:

    def get_departments_count(session: DBSession) -> int:
        count = session.query(Department).count()
        
        return count
    
    def get_departments_func_count(session: DBSession) -> int:
        count = session.query(func.count(Department.id)).scalar()
    
        return count


Многие разработчики используют функцию `count()` для проверки наличия данных в запросе. Это не очень хорошая практика, порождающая использование дополнительных ресурсов БД и увеличение времени выполнения запроса. Хорошим решением будет использование функции `exists()`, возвращающей скалярное значение:
lesson3:
    
    def check_department_exists(session: DBSession, department_name: str) -> bool:

        is_exists = session.query(exists().where(Department.name == department_name)).scalar()
    
        return is_exists
        
Двигаясь дальше, усложним задачу и познакомимся с сущностью `relation` или `relationship`. Дело в том, что в `SQLAlchemy` кроме использования foreign_key 
на уровне базы данных, используются еще и отношения между объектами. 
Таким образом мы можем получить зависимую по foreign key строку БД в объекте.
Эти объекты являются проекцией на таблицы БД, связанные между собой.

`Relations` в `SQLAlchemy` имеют гибкую настройку, позволяя получать данные из БД разными способами в разное время с помощью именованного аргумента `lazy`. 
Основные степени "ленивости":

* `select` - по умолчанию. ORM делает запрос только тогда, когда обращаются к данным. Осуществляется отдельным запросом.
* `dynamic` - позволяет получить объект запроса, который можно модифицировать по желанию. Получает данные из БД только после вызова all() или one() или любых других доступных методов.
* `joined` - в основной запрос добавляется с помощью LEFT JOIN. Выполняется сразу.
* `subquery` - похож на select, но выполняется как подзапрос.

По умолчанию - `select`.

Фильтрация в запросах может быть статической и динамической. Динамическая фильтрация позволяет наполнить запрос фильтрами, которые могут изменяться в 
зависимости от хода выполнения функции.
lesson4:

    def dynamic_filter(session: DBSession, filter: DFilter = None):

        query = session.query(Employee)
    
        if filter is not None:
            query = query.filter(*filter.conds)
    
        employees = query.all()
    
        return employees
        
В классе фильтра DFilter указаны фильтры на основе каких-либо входных данных. Если класс фильтра определён, но далее в запросе применяются условия.
Функция .filter() принимает принимает бинарные условия SQLAlchemy, поэтому может быть представлена с помощью * 
Применение динамических фильтров ограничивается только фантазией. Результат выполнения запроса показывает, какие герои сейчас неактивны.
 
    output:
        Inactive_heros:
            Name: Tony Stark
            Name: Scott Lang
            Name: Peter Parker    
        

Предлагаю поработать с отношением many-to-many.
Мы имеем таблицу Employee, в которой присутствует relation к таблице соответствий EmployeesSkills. Она содержит foreign_key на таблицу сотрудников и foreign_key
на таблицу умений.
lesson 5:
    
    def get_employee_with_skills(session: DBSession, eid: int):
        employee = session.query(EmployeeWithSkills).filter(EmployeeWithSkills.id == eid).one()
    
        return employee
    
    output:
        Employee Tony Stark has skills:
        Skill: Fly, Desc: I belive I can Fly. I belive I can touch the sky
        Skill: Light Shield, Desc: Light protect. Perfect for everything

Используя класс EmployeeWithSkills в запросе выше, мы обращаемся к нему, как к таблице БД, но на самом деле такой таблицы не существует. Это класс отличается от Employee наличие relation, которое имеет отношение many-to-many. Так мы можем разграничивать логику работы классов, наполняя разным набором relations. В результате запроса мы увидим умения одного из сотрудников.

Так как сотрудник может состоять в нескольких подразделениях, создадим relation, позволяющий получить эту информацию.
Создадим класс EmployeeWithDepartments, наследуемый от Employee и добавим следующее:

    class EmployeeWithDepartments(Employee):
        departments = relation(
            Department,
            # primaryjoin=EmployeeDepartments.employee_id == Employee.id,
            secondary=EmployeeDepartments.__tablename__,
            # secondaryjoin=EmployeeDepartments.department_id == Department.id,
        )
        
Созданный класс не является новой таблицей БД. Это все та же таблица Employee, только расширенная c помощью `relation`. Таким образом, вы можете обращаться к таблице `Employee` или `EmployeeWithDepartments` в запросах. Разница будет лишь в отсутствии/наличии `relation`.
    
Первый аргумент указывает к какой таблице мы будем создавать `relation`.
`primaryjoin` - это условие, по которому будет подключаться вторая таблица до её присоединения к объекту.
`secondary` - имя таблицы, содержащее foreign_keys для сопоставления. Используется в случае many-to-many.
`secondaryjoin` - условия сопоставления промежуточной таблицы с последней.

`primaryjoin` и `secondaryjoin` служат для явного указания соответствий в сложных ситуациях.

Порой возникают ситуации, когда необходимо создавать фильтры, поля которых объявлены в отношениях, а отношения в свою очередь являются отношениями исходного класса.
    
    EmployeeWithCadreMovements -> relation(CadreMovement) -> field
    
Если отношение отображает список значений, то нужно использовать .any(), если значение предусмотрено только одно, то необходимо использовать .has()
Для лучшего понимания, данная конструкция будет интерпретирована на SQL языка в конструкцию exists().
Вызовем функцию получения с указанием параметра причины `reason`, например, `simple`.
    
lesson6

    def has_in_relations(session: DBSession, reason: str):
        employees = session.query(EmployeeWithCadreMovements).filter(EmployeeWithCadreMovements.cadre_movements.any(CadreMovement.reason == reason)).all()
        return employees
        
    output:
        [Steve Rogers, Tony Stark]


lession7

Рассмотрим возможность получения relation с помощью функции агрегации. Например, получим последнее кадровое движение определенного пользователя.
primaryjoin является условием присоединения таблиц (в случае использования lazy='joined'). Напомним, что по умолчанию используется select.
В этом случае, формируется отдельный запрос при обращении к атрибуту класса. Именно для этого запроса мы и можем указать условия фильтрации.
Как известно, нельзя использовать функции агрегации в "чистом" виде в WHERE условии, поэтому мы можем реализовать данную возможность, указав relation 
со следующими параметрами:
    
    last_cadre_movement = relation(
        CadreMovement,
        primaryjoin=and_(
            CadreMovement.employee == Employee.id,
            uselist=False,
            CadreMovement.id == select([func.max(CadreMovement.id)]).where(CadreMovement.employee == Employee.id)
        )
    )

При выполнении запрос скомпилируется так:

    SELECT 
        cadre_movements.id AS cadre_movements_id, 
        cadre_movements.created_at AS cadre_movements_created_at, 
        cadre_movements.updated_at AS cadre_movements_updated_at, 
        cadre_movements.employee AS cadre_movements_employee, 
        cadre_movements.old_department AS cadre_movements_old_department, 
        cadre_movements.new_department AS cadre_movements_new_department, 
        cadre_movements.reason AS cadre_movements_reason 
    FROM cadre_movements 
    WHERE cadre_movements.employee = %(param_1)s 
        AND cadre_movements.id = (
            SELECT max(cadre_movements.id) AS max_1 
            FROM cadre_movements 
             WHERE cadre_movements.employee = %(param_1)s
        )

[Ссылка на github](https://github.com/sandix90/sqlalchemy_basics)

ИТОГ:
SQLAlchemy является мощнейшим инструментом в построении запросов, который уменьшает время разработки, поддерживая наследование.
Но стоит соблюдать тонкую грань между использованием ORM и написанием сложных запросов. В некоторых случаях ORM может запутать разработчика или сделать код громоздким и нечитаемым.
Удачи!


