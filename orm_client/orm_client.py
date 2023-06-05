import uuid
import allure
import structlog
from sqlalchemy import create_engine

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


class OrmClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f'postgresql://{user}:{password}@{host}/{database}'
        print(connection_string)
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def close_connection(self):
        self.db.close()

    def send_query(self, query):
        with allure.step("Печать запроса и лога"):
            print(query)
            log = self.log.bind(event_id=str(uuid.uuid4()))
            log.msg(
                event='request',
                query=str(query)
            )
        with allure.step("Выполнение запроса и вывод ответа"):
            dataset = self.db.execute(statement=query)
            result = [row for row in dataset]
            log.msg(
                event='response',
                dataset=[dict(row) for row in result]
            )
        return result

    def send_bulk_query(self, query):
        with allure.step("Печать запроса и лога"):
            print(query)
            log = self.log.bind(event_id=str(uuid.uuid4()))
            log.msg(
                event='request',
                query=str(query)
            )
        with allure.step("Выполнение запроса"):
            self.db.execute(statement=query)

