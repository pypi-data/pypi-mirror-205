class DBException(Exception):
    def __init__(self, exception, query):
        self.exception = exception
        self.query = query


def cursor(func):
    def wrapper(self, *args, **kwargs):
        if "sql_cursor" in kwargs:
            return func(*args, **kwargs)
        cur = self.connection.cursor()
        result = func(self, *args, sql_cursor=cur, **kwargs)
        cur.close()
        return result
    return wrapper


class TMKTPostgresql:

    def __init__(self, dbname, user, password, host, port, driver, cursor_factory):
        self.driver = driver
        self.connection = self.connect(dbname=dbname, user=user, password=password,
                                       host=host, port=port, cursor_factory=cursor_factory)
        self.connection.autocommit = True

    @staticmethod
    def execute(sql_cursor, sql, params):
        try:
            sql_cursor.execute(sql, params)
        except Exception as e:
            raise DBException(e, sql_cursor.query)
        return sql_cursor

    @cursor
    def exec(self, sql: str, params=None, sql_cursor=None):
        self.execute(sql_cursor, sql, params)

    @cursor
    def one(self, sql: str, params=None, sql_cursor=None):
        self.execute(sql_cursor, sql, params)
        return sql_cursor.fetchone()

    @cursor
    def all(self, sql: str, params=None, sql_cursor=None):
        self.execute(sql_cursor, sql, params)
        return sql_cursor.fetchall()

    def close(self):
        self.connection.close()

    def connect(self, dbname, user, password, host, port, cursor_factory):
        return self.driver.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            cursor_factory=cursor_factory
        )
