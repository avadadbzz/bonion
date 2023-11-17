import psycopg2
from psycopg2 import sql, pool
from psycopg2.extras import RealDictCursor

class PostgresLoader:
    def __init__(self, dbname, user, password, host, port, minconn=1, maxconn=10):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.minconn = minconn
        self.maxconn = maxconn

    def get_conn(self, dict_cursor=False):
        cursor_factory = RealDictCursor if dict_cursor else None
        return psycopg2.pool.SimpleConnectionPool(self.minconn, self.maxconn, dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port, cursor_factory=cursor_factory).getconn()

    def load_dict(self, schema, table, data_dicts):
        conn = self.get_conn(dict_cursor=True)
        try:
            with conn.cursor() as cur:
                for data_dict in data_dicts:
                    columns = data_dict.keys()
                    values = [data_dict[column] for column in columns]
                    insert = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
                        sql.Identifier(schema,table),
                        sql.SQL(',').join(map(sql.Identifier, columns)),
                        sql.SQL(',').join(map(sql.Placeholder, columns))
                    )
                    cur.execute(insert, data_dict)
                conn.commit()
                print("Success Insert")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            print("Connection closed")

    def get(self, query, params=None, dict_cursor=False):
        conn = self.get_conn(dict_cursor)
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                return {'data': rows}
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()